#!/usr/bin/env python3
"""validate_pdp.py - lint a Product Description Writer master copy.

Enforces the checkable rules from SKILL.md and references/:
  structure  - hook budget, 3-5 benefit bullets, benefit-restating CTA, Details block
  voice      - sentence length, bullet length, payoff front-loading, exclamation use
  claims     - vague filler, unsubstantiated claims, fake urgency, absolute language

It does NOT compare the copy against the source spec sheet - that is
spec_coverage.py's job.

Usage:
    python validate_pdp.py draft.md
    python validate_pdp.py draft.md --strict --json
    cat draft.md | python validate_pdp.py -

Exit codes: 0 clean, 1 errors found, 2 usage/IO problem.
Stdlib only, Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

try:  # keep CJK output readable on legacy Windows consoles
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

# --------------------------------------------------------------------------- #
# Lexicons
# --------------------------------------------------------------------------- #

# Generic openers / category claims that must never lead a PDP (SKILL.md Do NOT).
BANNED_HOOKS = [
    r"\bpremium quality\b", r"\bhigh[-\s]?quality\b", r"\bhigh[-\s]?end\b",
    r"\bworld[-\s]?class\b", r"\bbest[-\s]in[-\s]class\b",
    r"\bstate[-\s]of[-\s]the[-\s]art\b", r"\bcutting[-\s]edge\b",
    r"\bintroducing\b", r"\bsay hello to\b", r"\bmeet the\b", r"\bwelcome to\b",
    r"\bthe ultimate\b", r"\bthe perfect\b", r"\bpremium\b",
    r"\bmodern design\b", r"\belegant design\b",
]

# Vague words anywhere in the sell copy: they assert nothing testable.
VAGUE_TERMS = [
    r"\bpremium quality\b", r"\bhigh[-\s]?quality\b", r"\btop[-\s]?quality\b",
    r"\bpremium materials?\b", r"\bquality materials?\b",
    r"\bdurable construction\b", r"\bhigh performance\b", r"\bhigh[-\s]?performance\b",
    r"\beasy to use\b", r"\buser[-\s]friendly\b", r"\bversatile\b", r"\bergonomic\b",
    r"\binnovative\b", r"\badvanced technology\b",
    r"\bperfect for (?:home|everyone|any)\b", r"\bsuitable for all\b",
    r"\bone size fits all\b", r"\bdesigned for everyone\b",
]

# Claims that need substantiation the source usually lacks (compliance doc §1).
CLAIM_TERMS = [
    r"\bguaranteed\b", r"\bclinically proven\b", r"\bclinically tested\b",
    r"\bdermatologist (?:tested|recommended|approved)\b", r"\bdoctor recommended\b",
    r"\bFDA approved\b", r"\bmedical[-\s]grade\b", r"\bcures?\b", r"\btreats?\b",
    r"\bheals?\b", r"\bprevents?\b", r"\beliminates?\b", r"\bkills? 99(?:\.9)?%",
    r"\banti[-\s]?bacterial\b", r"\bnon[-\s]?toxic\b", r"\bhypoallergenic\b",
    r"\bsafe for (?:all|babies|kids|children)\b", r"\bbiodegradable\b",
    r"\bcarbon[-\s]neutral\b", r"\beco[-\s]?friendly\b", r"\bsustainable\b",
    r"\bplanet[-\s]?positive\b", r"\b100% (?:natural|pure|safe|effective)\b",
    r"\bpermanent(?:ly)?\b", r"\bnever fails?\b", r"\blifetime guarantee\b",
    r"\brisk[-\s]free\b",
]

# Fake-urgency patterns (compliance doc §5).
URGENCY_TERMS = [
    r"\blimited[-\s]time\b", r"\bselling fast\b", r"\bonly \d+ left\b",
    r"\b(?:today|tonight|this week) only\b", r"\blast chance\b",
    r"\bwhile (?:supplies|stocks) last\b", r"\border (?:now|in the next)\b",
    r"\bexpires? (?:today|tonight|soon)\b", r"\bflash sale\b", r"\bhurry\b",
    r"\bdon'?t miss out\b", r"\balmost gone\b",
]

# Absolute language prohibited under China's advertising law (compliance doc §2).
# Only the highest-precision forms are listed; the doc's full table is the rule.
ABSOLUTE_CJK = [
    "最好", "最佳", "最优", "最强", "最便宜", "最低价", "最先进", "最新科技",
    "第一", "唯一", "独家", "首创", "国家级", "世界级", "顶级", "极致",
    "100%", "彻底", "完全恢复", "永久有效", "永久免费", "终身有效", "终身免费",
    "根治", "特效", "药到病除", "无任何副作用", "无副作用",
    "全网最低", "秒杀全网", "史无前例", "绝对安全", "零风险",
]

BARE_CTAS = [
    "buy now", "shop now", "add to cart", "order now", "order today",
    "get yours", "get it now", "purchase now", "buy today", "shop today",
    "checkout", "add to basket",
]
CTA_VERB_RE = re.compile(
    r"\b(buy|shop|order|add to (?:cart|basket)|purchase|checkout|get it)\b", re.I
)

# --------------------------------------------------------------------------- #
# Text helpers
# --------------------------------------------------------------------------- #

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3000-\u303f\uff00-\uffef]")
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'\u2019\-]*")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?\u2026])\s+|\n+|(?<=[\u3002\uff01\uff1f\uff1b])")
BULLET_RE = re.compile(r"^\s*(?:[-*\u2022\u2023\u25cf\u25aa]|\d+[.)\u3001])\s+")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*\S)\s*$")
BOLD_LEAD_RE = re.compile(r"^\s*(?:[-*\u2022\u2023\u25cf\u25aa]|\d+[.)\u3001])\s*\*\*(.+?)\*\*")
COMMENT_MARKER_RE = re.compile(r"^\s*<!--\s*([A-Za-z][A-Za-z \-]{1,24}?)\s*-->\s*$")

SECTION_ALIASES = {
    "hook": ["hook", "headline", "lead", "标题", "主标题"],
    "intro": ["intro", "introduction", "lede", "opening", "简介", "引言"],
    "benefits": ["benefits", "benefit", "bullets", "卖点", "亮点", "优势"],
    "goodtoknow": [
        "good to know", "good-to-know", "objections", "notes", "before you buy",
        "值得知道", "须知", "购买须知", "注意事项", "温馨提示", "小提示", "你需要知道的",
    ],
    "cta": ["cta", "call to action", "closing", "行动号召"],
    "details": [
        "details", "specs", "specifications", "product details", "spec",
        "规格", "规格参数", "产品参数", "参数", "详情", "明细", "规格表",
    ],
}
ALIAS_TO_SECTION = {a: k for k, v in SECTION_ALIASES.items() for a in v}


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "rb") as fh:
        raw = fh.read()
    for enc in ("utf-8-sig", "utf-8", "gb18030", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def has_cjk(text: str) -> bool:
    return bool(CJK_RE.search(text))


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def length_units(text: str) -> int:
    """Latin: words. CJK: Han characters (punctuation excluded). Mixed: both summed."""
    han = len(HAN_RE.findall(text))
    latin = len(WORD_RE.findall(HAN_RE.sub(" ", text)))
    return han + latin


def is_cjk_heavy(text: str) -> bool:
    """More Han characters than latin words -> CJK budgets apply."""
    return len(HAN_RE.findall(text)) >= max(4, word_count(text))


def sentences(text: str) -> List[str]:
    parts = [p.strip() for p in SENTENCE_SPLIT_RE.split(text)]
    return [p for p in parts if p and not BULLET_RE.match(p)]


def syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1 and not w.endswith(("le", "ee", "ye")):
        n -= 1
    return max(1, n)


def normalise_latin(text: str) -> str:
    return re.sub(r"[\u2018\u2019]", "'", re.sub(r"[\u201c\u201d]", '"', text)).lower()


def undecorate(line: str) -> str:
    """'**Details**' -> 'Details';  '## Good to know' -> 'Good to know'."""
    t = line.strip().strip("*_#>").strip().strip("*_").strip()
    return t


def label_index(lines: List[str], section: str, max_len: int = 24) -> Optional[int]:
    """Index of a standalone section label line such as 'Good to know' or '**Details**'."""
    for i, line in enumerate(lines):
        if BULLET_RE.match(line):
            continue
        t = undecorate(line).rstrip(":").strip()
        if not t or len(t) > max_len:
            continue
        if ALIAS_TO_SECTION.get(t.lower()) == section:
            return i
    return None


# --------------------------------------------------------------------------- #
# Section parsing
# --------------------------------------------------------------------------- #

@dataclass
class Sections:
    hook: str = ""
    intro: str = ""
    benefits: List[str] = None  # type: ignore[assignment]
    goodtoknow: str = ""
    cta: str = ""
    details: str = ""
    detected_by: str = "heuristic"

    def __post_init__(self) -> None:
        if self.benefits is None:
            self.benefits = []

    @property
    def prose(self) -> str:
        """Hook + intro + CTA + any non-bullet lines in Good to know."""
        notes = "\n".join(
            ln for ln in self.goodtoknow.splitlines()
            if ln.strip() and not BULLET_RE.match(ln)
        )
        return "\n".join(p for p in [self.hook, self.intro, self.cta, notes] if p)

    @property
    def sell_text(self) -> str:
        """Blocks 1-3 and 5: the copy that carries the sale (notes excluded)."""
        return "\n".join(p for p in [self.hook, self.intro, "\n".join(self.benefits), self.cta] if p)


def _marker_sections(lines: List[str]) -> Optional[Dict[str, List[str]]]:
    """Explicit markers only: <!-- hook --> ... or '## Benefits'."""
    found: List[Tuple[int, str]] = []
    for i, line in enumerate(lines):
        candidate: Optional[str] = None
        m = HEADING_RE.match(line)
        if m:
            candidate = m.group(1)
        else:
            cm = COMMENT_MARKER_RE.match(line)
            if cm:
                candidate = cm.group(1)
        if candidate is None:
            continue
        key = ALIAS_TO_SECTION.get(candidate.strip().lower().rstrip(":"))
        if key:
            found.append((i, key))
    # A single stray heading is not a template - require a real marker set.
    if len(found) < 3:
        return None
    out: Dict[str, List[str]] = {}
    for idx, (start, key) in enumerate(found):
        end = found[idx + 1][0] if idx + 1 < len(found) else len(lines)
        out.setdefault(key, []).extend(lines[start + 1:end])
    return out


def _details_start(lines: List[str]) -> Optional[int]:
    idx = label_index(lines, "details")
    if idx is not None:
        return idx
    for i, line in enumerate(lines):
        if re.match(r"^\s*<!--\s*(details|specs|specifications)\s*-->\s*$", line, re.I):
            return i
    # fallback: the last contiguous block dominated by 'Label: value' lines
    best: Optional[int] = None
    i, n = 0, len(lines)
    while i < n:
        if not lines[i].strip():
            i += 1
            continue
        j = i
        while j < n and lines[j].strip():
            j += 1
        block = lines[i:j]
        if len(block) >= 3:
            colon_rows = sum(1 for b in block if ":" in b or "\uff1a" in b)
            if colon_rows / len(block) >= 0.6:
                best = i
        i = j
    return best


def parse_sections(text: str) -> Sections:
    lines = text.splitlines()
    marked = _marker_sections(lines)
    s = Sections()
    if marked:
        s.detected_by = "markers"
        s.hook = "\n".join(marked.get("hook", [])).strip()
        s.intro = "\n".join(marked.get("intro", [])).strip()
        s.benefits = [ln.strip() for ln in marked.get("benefits", []) if BULLET_RE.match(ln)]
        s.goodtoknow = "\n".join(marked.get("goodtoknow", [])).strip()
        s.cta = "\n".join(marked.get("cta", [])).strip()
        s.details = "\n".join(marked.get("details", [])).strip()
        return s

    dstart = _details_start(lines)
    sell_lines = lines[:dstart] if dstart is not None else lines
    s.details = "\n".join(lines[dstart:]).strip() if dstart is not None else ""

    nonempty = [i for i, ln in enumerate(sell_lines) if ln.strip()]
    if not nonempty:
        return s
    s.hook = undecorate(sell_lines[nonempty[0]]) or sell_lines[nonempty[0]].strip()

    gtn = label_index(sell_lines, "goodtoknow")
    all_bullets = [i for i, ln in enumerate(sell_lines) if BULLET_RE.match(ln)]
    benefit_idx = [i for i in all_bullets if gtn is None or i < gtn]
    s.benefits = [sell_lines[i].strip() for i in benefit_idx]

    if benefit_idx:
        first_b, last_b = benefit_idx[0], benefit_idx[-1]
        s.intro = "\n".join(
            sell_lines[i].strip() for i in nonempty if nonempty[0] < i < first_b
        ).strip()
        tail_start = last_b + 1
    else:
        cut = gtn if gtn is not None else (nonempty[-1] + 1)
        s.intro = "\n".join(
            sell_lines[i].strip() for i in nonempty if nonempty[0] < i < cut
        ).strip()
        tail_start = cut
    if gtn is not None:
        tail_start = max(tail_start, gtn + 1)

    tail = [i for i in nonempty if i >= tail_start]
    if tail:
        s.cta = sell_lines[tail[-1]].strip()
        s.goodtoknow = "\n".join(sell_lines[i].strip() for i in tail[:-1]).strip()
    return s


# --------------------------------------------------------------------------- #
# Findings
# --------------------------------------------------------------------------- #

SEVERITY_ORDER = {"ERROR": 0, "WARN": 1, "INFO": 2}


@dataclass
class Finding:
    code: str
    severity: str
    message: str
    excerpt: str = ""


def check(text: str, args: argparse.Namespace) -> Tuple[List[Finding], Sections, Dict[str, object]]:
    s = parse_sections(text)
    f: List[Finding] = []
    latin = normalise_latin(text)

    # ---- structure -------------------------------------------------------
    if not s.hook:
        f.append(Finding("E101", "ERROR",
                         "No lead hook found - the first line must stand alone."))
    else:
        n = length_units(s.hook)
        limit = args.hook_max_cjk if is_cjk_heavy(s.hook) else args.hook_max
        if n > limit:
            f.append(Finding("E102", "ERROR", f"Hook is {n} units; budget is {limit}.", s.hook))
        for pat in BANNED_HOOKS:
            if re.search(pat, normalise_latin(s.hook)):
                f.append(Finding("E103", "ERROR",
                                 f"Hook opens with a banned generic/category claim (/{pat}/).",
                                 s.hook))
                break

    nb = len(s.benefits)
    if nb == 0:
        f.append(Finding("E104", "ERROR", "No benefit bullets found (need 3-5)."))
    elif not 3 <= nb <= 5:
        f.append(Finding("E104", "ERROR", f"{nb} benefit bullets; the bar is 3-5."))

    if not s.cta:
        f.append(Finding("E107", "ERROR", "No CTA line found."))
    else:
        cta_norm = re.sub(r"[^\w\s']", "", normalise_latin(s.cta)).strip()
        bare = cta_norm in BARE_CTAS or (
            length_units(s.cta) <= 4 and CTA_VERB_RE.search(s.cta)
        )
        if bare:
            f.append(Finding("E108", "ERROR",
                             "CTA is a bare call to action - restate the benefit first.", s.cta))

    if not s.details:
        f.append(Finding("E109", "ERROR",
                         "No Details/Specs block found - spec-hunters cannot verify anything."))

    # ---- voice / readability --------------------------------------------
    for ln in s.benefits:
        lead = BOLD_LEAD_RE.match(ln)
        if not lead:
            f.append(Finding("E105", "ERROR",
                             "Bullet has no bold payoff in its first words.", ln))
        else:
            bw = length_units(lead.group(1))
            if bw > args.bold_max:
                f.append(Finding("W206", "WARN",
                                 f"Bold payoff is {bw} units; keep it to {args.bold_max}.",
                                 ln))
        n = length_units(ln)
        limit = args.bullet_max_cjk if is_cjk_heavy(ln) else args.bullet_max
        if n > limit:
            f.append(Finding("W207", "WARN", f"Bullet is {n} units; budget is {limit}.", ln))

    intro_sents = sentences(s.intro)
    if s.intro and not 2 <= len(intro_sents) <= 3:
        f.append(Finding("W205", "WARN",
                         f"Intro has {len(intro_sents)} sentences; the bar is 2-3.",
                         intro_sents[0] if intro_sents else ""))

    if not s.goodtoknow and nb:
        f.append(Finding("W208", "WARN",
                         "No 'Good to know' / objections block - remaining doubts are unanswered."))

    prose = s.prose
    for sent in [x for x in sentences(prose) if length_units(x) > 2]:
        n = length_units(sent)
        limit = args.sentence_max_cjk if is_cjk_heavy(sent) else args.sentence_max
        if n > limit:
            sev = "ERROR" if n > limit * 1.6 else "WARN"
            f.append(Finding("E110" if sev == "ERROR" else "W210", sev,
                             f"Sentence is {n} units; budget is {limit}.", sent))

    bangs = s.sell_text.count("!") + s.sell_text.count("\uff01")
    if bangs > args.max_bangs:
        f.append(Finding("W211", "WARN",
                         f"{bangs} exclamation marks in the sell copy; keep at most {args.max_bangs}."))

    # ---- claim lexicon ---------------------------------------------------
    for pat in VAGUE_TERMS:
        m = re.search(pat, latin)
        if m:
            f.append(Finding("W201", "WARN", f"Vague/untestable phrase (/{pat}/).", m.group(0)))
    for pat in CLAIM_TERMS:
        m = re.search(pat, latin)
        if m:
            f.append(Finding("W202", "WARN",
                             f"Claim needs substantiation from the source (/{pat}/).", m.group(0)))
    for pat in URGENCY_TERMS:
        m = re.search(pat, latin)
        if m:
            f.append(Finding("W203", "WARN",
                             f"Urgency must be true and verifiable (/{pat}/). "
                             "Cite the source or cut it.", m.group(0)))
    if has_cjk(text):
        for term in ABSOLUTE_CJK:
            if term in text:
                f.append(Finding("W204", "WARN",
                                 f"Absolute language prohibited by advertising law: {term}", term))

    # ---- metrics ---------------------------------------------------------
    sell_text = s.sell_text
    sell_units = length_units(sell_text)
    prose_units = length_units(prose)
    note_units = length_units(s.goodtoknow)
    body_sents = [x for x in sentences(prose) if length_units(x) > 2] or [""]
    sents = max(1, len(body_sents))
    cjk_doc = is_cjk_heavy(prose) or is_cjk_heavy(s.hook)
    if cjk_doc:
        flesch: Optional[float] = None
        min_sell, max_sell, max_note = args.min_sell_cjk, args.max_sell_cjk, args.max_note_cjk
        unit_label = "CJK chars + latin words"
    else:
        syl = sum(syllables(w) for w in WORD_RE.findall(prose))
        flesch = (round(206.835 - 1.015 * (prose_units / sents)
                       - 84.6 * (syl / max(1, prose_units)), 1) if prose_units else None)
        min_sell, max_sell, max_note = args.min_sell, args.max_sell, args.max_note
        unit_label = "words"
    metrics: Dict[str, object] = {
        "sell_units": sell_units,
        "note_units": note_units,
        "bullets": nb,
        "prose_sentences": sents,
        "avg_sentence_units": round(prose_units / sents, 1),
        "flesch_reading_ease": flesch,
        "counting": unit_label,
        "sections_detected_by": s.detected_by,
    }
    if flesch is not None and prose_units and flesch < 55:
        f.append(Finding("I301", "INFO",
                         f"Flesch reading ease {flesch:.0f} - consumer PDP copy usually reads easier."))
    if sell_units and not min_sell <= sell_units <= max_sell:
        f.append(Finding("I302", "INFO",
                         f"Sell copy (hook+intro+bullets+CTA) is {sell_units} {unit_label}; "
                         f"the budget is {min_sell}-{max_sell}."))
    if note_units > max_note:
        f.append(Finding("I303", "INFO",
                         f"Good-to-know block is {note_units} {unit_label}; keep it under {max_note}."))

    return f, s, metrics


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #

COLOURS = {"ERROR": "\033[31m", "WARN": "\033[33m", "INFO": "\033[36m", "RESET": "\033[0m"}


def render(findings: List[Finding], metrics: Dict[str, object], use_colour: bool) -> str:
    out: List[str] = []
    counts = {sev: sum(1 for x in findings if x.severity == sev) for sev in ("ERROR", "WARN", "INFO")}
    if findings:
        for sev in ("ERROR", "WARN", "INFO"):
            group = [x for x in findings if x.severity == sev]
            if not group:
                continue
            head = f"{sev} ({len(group)})"
            if use_colour:
                head = f"{COLOURS[sev]}{head}{COLOURS['RESET']}"
            out.append(head)
            for fd in group:
                out.append(f"  [{fd.code}] {fd.message}")
                if fd.excerpt:
                    snip = fd.excerpt.strip().replace("\n", " ")
                    if len(snip) > 110:
                        snip = snip[:107] + "..."
                    out.append(f"        > {snip}")
            out.append("")
    else:
        out.append("No findings. Copy meets the bar.\n")
    flesch = metrics.get("flesch_reading_ease")
    out.append(
        "Metrics: {su} sell units / {nu} note units / {b} bullets"
        " / avg {avg} per sentence / Flesch {fl}".format(
            su=metrics.get("sell_units", "-"), nu=metrics.get("note_units", "-"),
            b=metrics.get("bullets", "-"), avg=metrics.get("avg_sentence_units", "-"),
            fl=(f"{flesch:.1f}" if isinstance(flesch, float) else "n/a (CJK)"),
        )
    )
    out.append(f"Summary: {counts['ERROR']} errors, {counts['WARN']} warnings, {counts['INFO']} notes")
    return "\n".join(out)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(
        prog="validate_pdp.py",
        description="Lint a PDP master copy against the Product Description Writer quality bar.",
    )
    p.add_argument("path", help="draft file (.md/.txt), or - for stdin")
    p.add_argument("--hook-max", type=int, default=12, help="latin words allowed in the hook (default 12)")
    p.add_argument("--hook-max-cjk", type=int, default=24, help="CJK chars allowed in the hook (default 24)")
    p.add_argument("--bullet-max", type=int, default=16, help="latin words allowed per bullet (default 16)")
    p.add_argument("--bullet-max-cjk", type=int, default=32, help="CJK chars allowed per bullet (default 32)")
    p.add_argument("--bold-max", type=int, default=4, help="words allowed in the bold payoff (default 4)")
    p.add_argument("--sentence-max", type=int, default=20, help="latin words allowed per sentence (default 20)")
    p.add_argument("--sentence-max-cjk", type=int, default=40, help="CJK chars allowed per sentence (default 40)")
    p.add_argument("--max-bangs", type=int, default=1, help="exclamation marks allowed in sell copy (default 1)")
    p.add_argument("--min-sell", type=int, default=80, help="minimum sell-copy words (default 80)")
    p.add_argument("--max-sell", type=int, default=160, help="maximum sell-copy words (default 160)")
    p.add_argument("--max-note", type=int, default=60, help="maximum Good-to-know words (default 60)")
    p.add_argument("--min-sell-cjk", type=int, default=120,
                   help="minimum sell-copy units for CJK copy (default 120)")
    p.add_argument("--max-sell-cjk", type=int, default=320,
                   help="maximum sell-copy units for CJK copy (default 320)")
    p.add_argument("--max-note-cjk", type=int, default=120,
                   help="maximum Good-to-know units for CJK copy (default 120)")
    p.add_argument("--strict", action="store_true", help="exit non-zero on warnings too")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--no-colour", "--no-color", dest="no_colour", action="store_true")
    args = p.parse_args(argv)

    try:
        text = read_text(args.path)
    except OSError as exc:
        print(f"cannot read {args.path}: {exc}", file=sys.stderr)
        return 2
    if not text.strip():
        print(f"{args.path} is empty", file=sys.stderr)
        return 2

    findings, sections, metrics = check(text, args)
    findings.sort(key=lambda x: (SEVERITY_ORDER[x.severity], x.code))

    if args.json:
        print(json.dumps({
            "file": args.path,
            "metrics": metrics,
            "findings": [asdict(x) for x in findings],
            "counts": {sev: sum(1 for x in findings if x.severity == sev)
                       for sev in ("ERROR", "WARN", "INFO")},
        }, ensure_ascii=False, indent=2))
    else:
        use_colour = (not args.no_colour) and sys.stdout.isatty() and not os.environ.get("NO_COLOR")
        print(render(findings, metrics, bool(use_colour)))

    errors = sum(1 for x in findings if x.severity == "ERROR")
    warns = sum(1 for x in findings if x.severity == "WARN")
    if errors:
        return 1
    if args.strict and warns:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
