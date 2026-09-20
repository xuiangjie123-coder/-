#!/usr/bin/env python3
"""spec_coverage.py - prove that a PDP master copy covers its source spec sheet.

The skill's quality bar says: spec-hunters must find every literal number in the
Details block, and every spec dropped from the sell copy must be logged. This
script checks the first half mechanically and produces the second half as a list.

Atom types extracted from the source:
  * numeric - 8.1 oz, 61 HRC, 15°, IPX7, ISO 24443, 3000 K, 21%, 67-layer, 12 x 8 in
  * named   - materials, treatments, certifications (316 stainless, AUS-10, NSF, USB-C)
  * text    - the prose half of a spec row (Origin, Warranty, Compatibility, Care)

For each atom it reports: present in the Details block, present in the body only,
or missing. Unit-equivalent conversions (8 in / 20.3 cm) are not reported as
unsourced numbers.

Usage:
    python spec_coverage.py spec.txt draft.md
    python spec_coverage.py spec.txt draft.md --json
    python spec_coverage.py spec.txt draft.md --allow-missing "67-layer,8.1 oz"
    python spec_coverage.py spec.txt draft.md --strict

Exit codes: 0 covered or acknowledged, 1 missing specs, 2 usage/IO problem.
Stdlib only, Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set, Tuple

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

# --------------------------------------------------------------------------- #
# Units
# --------------------------------------------------------------------------- #

UNIT_CANON = {
    "mm": "mm", "cm": "cm", "in": "in", "inch": "in", "inches": "in",
    '"': "in", "\u2033": "in", "ft": "ft", "foot": "ft", "feet": "ft",
    "g": "g", "gram": "g", "grams": "g", "kg": "kg", "mg": "mg",
    "oz": "oz", "ounce": "oz", "ounces": "oz", "lb": "lb", "lbs": "lb",
    "pound": "lb", "pounds": "lb",
    "ml": "ml", "l": "l", "liter": "l", "litre": "l", "floz": "floz", "fl oz": "floz",
    "w": "w", "watt": "w", "watts": "w", "v": "v", "volt": "v", "volts": "v",
    "amp": "a", "amps": "a",
    "mah": "mah", "wh": "wh", "hz": "hz", "khz": "khz", "ghz": "ghz",
    "lm": "lm", "lumen": "lm", "lumens": "lm", "db": "db", "rpm": "rpm",
    "psi": "psi", "bar": "bar", "gsm": "gsm", "ct": "ct", "qt": "qt", "gal": "gal",
    "pcs": "pcs", "pc": "pcs", "piece": "pcs", "pieces": "pcs",
    "pack": "pack", "count": "count", "layer": "layer", "layers": "layer",
    "ply": "ply", "blade": "blade", "blades": "blade", "speed": "speed",
    "speeds": "speed", "mode": "mode", "modes": "mode", "joint": "joint", "joints": "joint",
    "step": "step", "steps": "step", "hrc": "hrc", "micron": "micron",
    "\u00b5m": "micron", "um": "micron",
    "h": "h", "hr": "h", "hrs": "h", "hour": "h", "hours": "h",
    "min": "min", "mins": "min", "minute": "min", "minutes": "min",
    "s": "s", "sec": "s", "secs": "s", "second": "s", "seconds": "s",
    "day": "day", "days": "day", "week": "week", "weeks": "week",
    "month": "month", "months": "month", "year": "year", "years": "year",
    "yr": "year", "yrs": "year",
    "\u00b0": "deg", "\u00b0c": "degc", "\u00b0f": "degf",
}

# Ambiguous single letters (m, a, k) are intentionally excluded outside these contexts.
_UNITS_ALT = (
    "mm|cm|inches|inch|in|ft|feet|foot|kg|mg|g|lbs|lb|oz|fl\\.?\\s?oz|ml|l|"
    "watts?|w|volts?|v|amps?|mah|wh|khz|ghz|hz|lumens?|lm|cri|db|rpm|psi|bar|"
    "gsm|qt|gal|pcs|pieces?|pc|pack|count|ct|"
    "layers?|ply|blades?|speeds?|modes?|joints?|steps?|hrc|"
    "hours?|hrs?|h|minutes?|mins?|seconds?|secs?|days?|weeks?|months?|years?|yrs?|"
    "\u00b5m|um|micron|\u00b0c|\u00b0f|\u00b0|\u0022|\u2033"
)
NUM = r"\d+(?:[.,]\d+)?"

NUM_UNIT_RE = re.compile(rf"\b(?P<num>{NUM})\s*(?P<unit>{_UNITS_ALT})(?![A-Za-z])", re.I)
DIM_RE = re.compile(
    rf"\b(?P<num>{NUM})\s*[x\u00d7]\s*(?P<b>{NUM})(?:\s*[x\u00d7]\s*(?P<c>{NUM}))?"
    rf"(?:\s*(?P<unit>{_UNITS_ALT}))?(?![A-Za-z])",
    re.I,
)
RANGE_RE = re.compile(
    rf"\b(?P<a>{NUM})\s*[-\u2013\u2014]\s*(?P<b>{NUM})(?:\s*(?P<unit>{_UNITS_ALT}))?(?![A-Za-z])",
    re.I,
)
HYPHEN_UNIT_RE = re.compile(rf"\b(?P<num>{NUM})\s*-\s*(?P<unit>{_UNITS_ALT})(?![A-Za-z])", re.I)
SPF_RE = re.compile(r"\bspf\s*-?\s*(?P<num>\d+)", re.I)
KELVIN_RE = re.compile(r"\b(?P<num>\d{3,5})\s*K\b")
IP_RE = re.compile(r"\bIP[X0-9]{2}\b", re.I)
ISO_RE = re.compile(r"\bISO\s?\d{4,5}(?:-\d+)?\b", re.I)
PERCENT_RE = re.compile(rf"\b(?P<num>{NUM})\s*%")

# "<number> in" followed by one of these is prose ("3 in the box"), not a measurement.
_PROSE_GUARD = re.compile(r"^\s+(?:the|a|an|your|my|this|that|it|its|total)\b", re.I)

CERT_RE = re.compile(
    r"\b(?:RoHS|REACH|CE|FCC|FDA|NSF|UL|ETL|FSC|CARB|BSCI|GS|TUV|T\u00dcV|PSE|KC|"
    r"BPA[-\s]?free|PFAS[-\s]?free)\b",
    re.I,
)

NAMED_ATOMS = [
    "316 stainless steel", "316l stainless", "316 stainless", "304 stainless",
    "18/10 stainless", "stainless steel", "carbon steel", "damascus", "aus-10",
    "aluminum", "aluminium", "titanium", "carbon fiber", "carbon fibre", "brass",
    "copper", "cast iron", "zinc oxide",
    "silicone", "borosilicate glass", "tempered glass", "glass", "ceramic", "bamboo",
    "hemp", "linen", "merino", "wool", "organic cotton", "cotton", "polyester",
    "nylon", "leather", "pu leather", "abs", "eva", "tpe", "pakkawood", "acacia",
    "oak", "walnut", "maple", "non-nano",
    "dishwasher-safe", "dishwasher safe", "machine washable", "hand wash",
    "fragrance-free", "fragrance free", "alcohol-free", "non-comedogenic",
    "flicker-free", "flicker free", "full tang", "non-stick", "nonstick",
    "water-resistant", "water resistant",
    "niacinamide", "squalane", "hyaluronic acid", "retinol", "vitamin c", "shea butter",
    "usb-c", "usb c", "usb-a", "qi", "bluetooth 5.0", "bluetooth 5.1", "bluetooth 5.2",
    "bluetooth 5.3", "bluetooth 5.4", "wifi 6", "wi-fi 6", "nfc", "usb-c pd",
]

# Colon-less lines that are care/storage instructions rather than spec rows.
CARE_KW = re.compile(
    r"\b(?:hand wash|machine wash|washable|wash|dishwasher|wipe clean|wipe|care|"
    r"dry immediately|air dry|dry flat|avoid|do not|store|keep away|reapply|"
    r"apply generously|refrigerate|shelf life)\b",
    re.I,
)

LABEL_VALUE_RE = re.compile(r"^(?P<label>[^:]{1,30}):\s*(?P<v>.+)$")
# Rows that identify the product rather than describe it - not specs to verify.
NON_SPEC_LABELS = {
    "product", "item", "name", "title", "sku", "model", "brand", "category",
    "price", "msrp", "upc", "ean", "asin", "id", "code", "product name",
}
SECTION_ALIASES = {"details", "specs", "specifications", "product details", "spec"}
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*\S)\s*$")

# --------------------------------------------------------------------------- #
# Unit conversion (suppresses false "unsourced number" reports)
# --------------------------------------------------------------------------- #

_CONV_FAMILIES = [
    {"mm": 1.0, "cm": 10.0, "m": 1000.0, "in": 25.4, "ft": 304.8},                 # length
    {"mg": 0.001, "g": 1.0, "kg": 1000.0, "oz": 28.349523125, "lb": 453.59237},    # mass
    {"ml": 1.0, "l": 1000.0, "floz": 29.5735295625, "qt": 946.352946, "gal": 3785.411784},  # volume
]


def _equivalent(a: str, b: str) -> bool:
    """True if two number+unit tokens describe the same quantity (8in ~ 20.3cm)."""
    def split(tok: str) -> Optional[Tuple[float, str]]:
        m = re.fullmatch(r"(\d+(?:\.\d+)?)([a-z%]*)", tok)
        if not m:
            return None
        unit = m.group(2)
        try:
            return float(m.group(1)), unit
        except ValueError:
            return None

    sa, sb = split(a), split(b)
    if not sa or not sb or sa[1] == sb[1]:
        return False
    for fam in _CONV_FAMILIES:
        if sa[1] in fam and sb[1] in fam:
            va, vb = sa[0] * fam[sa[1]], sb[0] * fam[sb[1]]
            if vb == 0:
                return False
            return abs(va - vb) / max(va, vb) <= 0.02
    return False


# --------------------------------------------------------------------------- #
# Extraction
# --------------------------------------------------------------------------- #

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


def canon_unit(unit: str) -> str:
    u = re.sub(r"\s+", " ", unit.strip().lower().replace(".", ""))
    return UNIT_CANON.get(u, u)


def canon_num(num: str) -> str:
    n = num.replace(",", "")
    try:
        val = float(n)
    except ValueError:
        return n
    return str(int(val)) if val == int(val) else ("%g" % val)


def normalise(text: str) -> str:
    t = text.replace("\u00d7", "x").replace("\u2019", "'")
    t = re.sub(r"[\u2013\u2014]", "-", t)
    return re.sub(r"\s+", " ", t).lower()


@dataclass
class Atom:
    kind: str          # numeric | named | text
    raw: str           # as written in the source
    key: str           # normalised form used for matching
    parts: List[str] = field(default_factory=list)


def extract_numeric(text: str) -> List[Atom]:
    """Compound shapes run first so they are not shredded into bare numbers."""
    out: List[Atom] = []
    consumed: List[Tuple[int, int]] = []

    def taken(span: Tuple[int, int]) -> bool:
        return any(not (span[1] <= s or span[0] >= e) for s, e in consumed)

    def add(raw: str, key: str, parts: List[str], span: Tuple[int, int]) -> None:
        out.append(Atom("numeric", raw, key, parts))
        consumed.append(span)

    for m in DIM_RE.finditer(text):
        if taken(m.span()):
            continue
        nums = [canon_num(x) for x in (m.group("num"), m.group("b"), m.group("c")) if x]
        unit = canon_unit(m.group("unit")) if m.group("unit") else ""
        add(m.group(0).strip(), f"{'x'.join(nums)}{unit}", nums, m.span())

    for m in RANGE_RE.finditer(text):
        if taken(m.span()):
            continue
        unit = canon_unit(m.group("unit")) if m.group("unit") else ""
        nums = [canon_num(m.group("a")), canon_num(m.group("b"))]
        add(m.group(0).strip(), f"{'-'.join(nums)}{unit}", nums, m.span())

    for m in HYPHEN_UNIT_RE.finditer(text):
        if taken(m.span()):
            continue
        n = canon_num(m.group("num"))
        add(m.group(0).strip(), f"{n}{canon_unit(m.group('unit'))}", [n], m.span())

    for rx in (SPF_RE, KELVIN_RE, PERCENT_RE):
        for m in rx.finditer(text):
            if taken(m.span()):
                continue
            n = canon_num(m.group("num"))
            prefix = "" if rx is PERCENT_RE else ("spf" if rx is SPF_RE else "")
            suffix = "%" if rx is PERCENT_RE else ("k" if rx is KELVIN_RE else "")
            add(m.group(0).strip(), f"{prefix}{n}{suffix}", [n], m.span())

    for rx in (IP_RE, ISO_RE):
        for m in rx.finditer(text):
            if taken(m.span()):
                continue
            add(m.group(0).strip(), re.sub(r"\s+", "", m.group(0)).lower(), [], m.span())

    for m in NUM_UNIT_RE.finditer(text):
        if taken(m.span()):
            continue
        if canon_unit(m.group("unit")) == "in" and _PROSE_GUARD.match(text[m.end():]):
            continue
        n = canon_num(m.group("num"))
        add(m.group(0).strip(), f"{n}{canon_unit(m.group('unit'))}", [n], m.span())

    seen: Dict[str, Atom] = {}
    for a in out:
        seen.setdefault(a.key, a)
    return list(seen.values())


def extract_named(text: str) -> List[Atom]:
    low = normalise(text)
    out: List[Atom] = []
    for name in NAMED_ATOMS:
        if name in low:
            out.append(Atom("named", name, name))
    for m in CERT_RE.finditer(text):
        raw = re.sub(r"\s+", " ", m.group(0)).strip()
        out.append(Atom("named", raw, normalise(raw)))
    seen: Dict[str, Atom] = {}
    for a in out:
        seen.setdefault(a.key, a)
    return list(seen.values())


def extract_text(text: str) -> List[Atom]:
    """The prose half of a spec row, plus colon-less care instructions."""
    out: List[Atom] = []
    for line in text.splitlines():
        st = line.strip().lstrip("-*\u2022\u2023 ").strip()
        if len(st) < 4:
            continue
        m = LABEL_VALUE_RE.match(st)
        if m:
            if m.group("label").strip().lower() in NON_SPEC_LABELS:
                continue
            value = m.group("v").strip()
            if any(len(w) >= 4 for w in re.findall(r"[^\W\d_]+", value, re.UNICODE)):
                out.append(Atom("text", value, normalise(value)))
            continue
        if CARE_KW.search(st) and len(st) <= 90:
            out.append(Atom("text", st, normalise(st)))
    seen: Dict[str, Atom] = {}
    for a in out:
        seen.setdefault(a.key, a)
    return list(seen.values())


def unparsed_source_lines(src: str) -> List[str]:
    """Source lines the extractors understood nothing about - check these by hand."""
    out: List[str] = []
    for line in src.splitlines():
        st = line.strip()
        if len(st) < 4 or len(st.split()) < 2:
            continue
        if extract_numeric(st) or extract_named(st) or extract_text(st):
            continue
        out.append(st)
    return out


def details_region(draft: str) -> str:
    lines = draft.splitlines()
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m and m.group(1).strip().lower().rstrip(":") in SECTION_ALIASES:
            return "\n".join(lines[i:])
        if re.match(r"^\s*<!--\s*(details|specs|specifications)\s*-->\s*$", line, re.I):
            return "\n".join(lines[i:])
    # fallback: the last contiguous block dominated by 'Label: value' rows
    blocks: List[Tuple[int, int]] = []
    i = 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        j = i
        while j < len(lines) and lines[j].strip():
            j += 1
        blocks.append((i, j))
        i = j
    for start, end in reversed(blocks):
        block = lines[start:end]
        if len(block) >= 3:
            colon_rows = sum(1 for b in block if ":" in b or "\uff1a" in b)
            if colon_rows / len(block) >= 0.6:
                return "\n".join(lines[start:])
    return ""


# --------------------------------------------------------------------------- #
# Coverage
# --------------------------------------------------------------------------- #

@dataclass
class Result:
    kind: str
    raw: str
    status: str        # OK_DETAILS | BODY_ONLY | MISSING | ALLOWED
    where: str = ""


def _significant_words(text: str) -> List[str]:
    return [w for w in re.findall(r"[^\W\d_]{4,}", text, re.UNICODE)]


def coverage(atoms: List[Atom], draft: str, allow: Set[str]) -> Tuple[List[Result], List[str]]:
    details = details_region(draft)
    draft_all = normalise(draft)
    draft_details = normalise(details)

    draft_num = extract_numeric(draft)
    detail_num = extract_numeric(details)
    tokens_all = {a.key for a in draft_num}
    tokens_details = {a.key for a in detail_num}
    nums_all = {p for a in draft_num for p in a.parts}
    nums_details = {p for a in detail_num for p in a.parts}

    results: List[Result] = []
    for atom in atoms:
        if atom.key in allow or atom.raw.lower() in allow:
            results.append(Result(atom.kind, atom.raw, "ALLOWED", "acknowledged drop"))
            continue

        if atom.kind == "numeric":
            if atom.key in tokens_details:
                results.append(Result(atom.kind, atom.raw, "OK_DETAILS", "Details block"))
            elif atom.key in tokens_all:
                results.append(Result(atom.kind, atom.raw, "BODY_ONLY", "body copy only"))
            elif atom.parts and set(atom.parts) <= nums_details:
                results.append(Result(atom.kind, atom.raw, "OK_DETAILS", "numbers in Details"))
            elif atom.parts and set(atom.parts) <= nums_all:
                results.append(Result(atom.kind, atom.raw, "BODY_ONLY", "numbers in body"))
            else:
                gone = [p for p in atom.parts if p not in nums_all]
                note = "absent from draft" + (f" (no {', '.join(gone)})" if gone else "")
                results.append(Result(atom.kind, atom.raw, "MISSING", note))
            continue

        if atom.kind == "named":
            if atom.key in draft_details:
                results.append(Result(atom.kind, atom.raw, "OK_DETAILS", "Details block"))
            elif atom.key in draft_all:
                results.append(Result(atom.kind, atom.raw, "BODY_ONLY", "body copy only"))
            else:
                results.append(Result(atom.kind, atom.raw, "MISSING", "absent from draft"))
            continue

        # text atoms: half of the significant words present is enough
        words = _significant_words(atom.key)
        if not words:
            continue
        need = max(1, math.ceil(len(words) / 2))
        if sum(1 for w in words if w in draft_details) >= need:
            results.append(Result(atom.kind, atom.raw, "OK_DETAILS", "Details block"))
        elif sum(1 for w in words if w in draft_all) >= need:
            results.append(Result(atom.kind, atom.raw, "BODY_ONLY", "body copy only"))
        else:
            results.append(Result(atom.kind, atom.raw, "MISSING", "absent from draft"))

    src_tokens = {a.key for a in atoms if a.kind == "numeric"}
    unsourced = []
    for tok in sorted(tokens_all):
        if tok in src_tokens or tok.isdigit():
            continue
        if any(_equivalent(tok, s) for s in src_tokens):
            continue
        unsourced.append(tok)
    return results, unsourced


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

ICONS = {
    "OK_DETAILS": "[ok]      ",
    "BODY_ONLY":  "[body]    ",
    "MISSING":    "[MISSING] ",
    "ALLOWED":    "[allowed] ",
}
KIND_HEADER = [
    ("numeric", "NUMERIC ATOMS"),
    ("named", "NAMED ATOMS"),
    ("text", "TEXT ATOMS (care / origin / warranty / compatibility)"),
]


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(
        prog="spec_coverage.py",
        description="Check that a PDP master copy covers every spec in the source sheet.",
    )
    p.add_argument("source", help="source spec sheet (.txt/.md)")
    p.add_argument("draft", help="PDP master copy (.md/.txt), or - for stdin")
    p.add_argument("--allow-missing", default="",
                   help="comma-separated atoms intentionally dropped (acknowledges them)")
    p.add_argument("--strict", action="store_true",
                   help="also fail when a spec sits outside the Details block")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    args = p.parse_args(argv)

    try:
        src = read_text(args.source)
        draft = read_text(args.draft)
    except OSError as exc:
        print(f"cannot read input: {exc}", file=sys.stderr)
        return 2
    if not src.strip():
        print(f"{args.source} is empty - nothing to check.", file=sys.stderr)
        return 2
    if not draft.strip():
        print(f"{args.draft} is empty - nothing to check.", file=sys.stderr)
        return 2

    atoms = extract_numeric(src) + extract_named(src) + extract_text(src)
    allow = {a.strip().lower() for a in args.allow_missing.split(",") if a.strip()}
    results, unsourced = coverage(atoms, draft, allow)
    unparsed = unparsed_source_lines(src)

    counts = {k: sum(1 for r in results if r.status == k)
              for k in ("OK_DETAILS", "BODY_ONLY", "MISSING", "ALLOWED")}
    missing = [r for r in results if r.status == "MISSING"]

    if args.json:
        print(json.dumps({
            "source": args.source,
            "draft": args.draft,
            "counts": counts,
            "results": [asdict(r) for r in results],
            "unsourced_numbers": unsourced,
            "unparsed_source_lines": unparsed,
        }, ensure_ascii=False, indent=2))
    else:
        detail_region = details_region(draft)
        if not detail_region:
            print("WARNING: no Details/Specs block found in the draft - every atom below "
                  "can only be satisfied by body copy.\n")
        print(f"Source atoms: {len(atoms)}   "
              f"({counts['OK_DETAILS']} in Details, {counts['BODY_ONLY']} body-only, "
              f"{counts['MISSING']} missing, {counts['ALLOWED']} acknowledged)\n")
        for kind, header in KIND_HEADER:
            group = [r for r in results if r.kind == kind]
            if not group:
                continue
            print(header)
            for r in group:
                print(f"  {ICONS[r.status]} {r.raw[:60]:<60} {r.where}")
            print("")
        if unsourced:
            print("NUMBERS IN THE COPY WITH NO SOURCE")
            for tok in unsourced:
                print(f"  [verify]  {tok:<60} confirm against the sheet or remove")
            print("")
        if unparsed:
            print("SOURCE LINES WITH NO ATOM EXTRACTED (check these by hand)")
            for ln in unparsed:
                print(f"  [manual]  {ln[:60]}")
            print("")
        print(f"Verdict: {counts['MISSING']} missing, {counts['BODY_ONLY']} body-only, "
              f"{len(unsourced)} unsourced numbers")
        if missing:
            print("Log each missing atom in the delivery notes as a deliberate drop, "
                  "or move it into the copy.")

    if counts["MISSING"]:
        return 1
    if args.strict and counts["BODY_ONLY"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
