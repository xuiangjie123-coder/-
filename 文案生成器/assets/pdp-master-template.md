# PDP Master Template

Copy the block below and fill it. The delivered artifact is exactly this shape — no headings, no labels, no marketing chrome. It pastes into any CMS.

## Budgets

| Block | Budget (latin) | Budget (CJK) | Checked by |
|---|---|---|---|
| Hook | ≤ 12 words | ≤ 24 chars | E102 |
| Intro | 2–3 sentences, 25–50 words | 40–90 chars, 2–3 sentences | W205 |
| Benefit bullets | 3–5 × ≤ 16 words, bold payoff 2–4 words | 3–5 × ≤ 32 chars, bold payoff ≤ 4 字 | E104, E105, W206, W207 |
| Good to know | 2–4 lines, ≤ 60 words | ≤ 120 chars | W208, I303 |
| CTA | 1 line, benefit restated | 1 line | E107, E108 |
| Sell copy total (hook+intro+bullets+CTA) | 80–160 words | 120–320 chars | I302 |
| Details | unlimited, literal | unlimited | E109 |

**CJK payoff budget.** The bold payoff is counted in characters, not words — 4 字 上限. `**软地不陷。**`(4) passes; `**烂地压不弯。**`(5) trips W206. The Latin "2–4 words" rule does not translate: four English words can be 20+ characters, four Chinese characters carry the same punch. Write the payoff as a verb + object, then move every qualifier into the proof clause.

## Skeleton

```text
[HOOK — one line, ≤12 words, must work with nothing above it. No "premium", no category noun.]

[INTRO — 2-3 sentences. S1 = the transformation or the enemy. S2 = the one spec doing the work. S3 = who it is for, and who it is not for.]

- **[PAYOFF 2-4 words].**  [spec as proof, rest of the sentence ≤12 words.]
- **[PAYOFF 2-4 words].**  [spec as proof.]
- **[PAYOFF 2-4 words].**  [spec as proof.]

Good to know

- [objection answered honestly, one line]
- [the inconvenient truth that prevents a return]
- [compatibility / care / what is not included]

[CTA — restate the benefit, then the action. Never a bare "Buy now".]

**Details**

[Label]: [literal value]
[Label]: [literal value]
...
```

## Fill order

1. Hook last. Write the bullets first, then find the one thing they all point at.
2. Bullets: bridge test each candidate (`references/benefit-translation.md`), keep the 3–5 that pass, order strongest differentiator first.
3. Details: transcribe every row, including the unflattering ones. This block is a census, not a pitch.
4. Good to know: whatever is left over from `references/objection-library.md`.
5. CTA: read the hook again and answer it.

## Variants

**3 bullets** — one dominant differentiator, or a low-consideration purchase.
**5 bullets** — several comparable differentiators, or a high-consideration purchase.
**Never 6.** If a sixth benefit is real, one of the existing five is not.

**Short-form / marketplace-style field** — hook + 3 bullets + CTA, Details omitted. Note in the delivery notes that the spec-coverage check was not applied.

## Optional scratch markers

The validator parses the bare skeleton above by structure, so markers are not required. If a draft is unusual enough to confuse the parser, add these on their own lines, run the checks, then delete them before delivery:

```text
<!-- hook -->
<!-- intro -->
<!-- benefits -->
<!-- good-to-know -->
<!-- cta -->
<!-- details -->
```

## Pre-delivery

1. `python scripts/spec_coverage.py <spec> <draft>` — 0 missing, or each missing atom acknowledged.
2. `python scripts/validate_pdp.py <draft>` — 0 errors; read every warning out loud before dismissing it.
3. Append the two delivery-note lists: dropped specs, unsupported claims.
