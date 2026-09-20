# PDP Anatomy

The page is scanned in an F-pattern on a phone. Budgets below are the contract; `scripts/validate_pdp.py` enforces the checkable ones.

## Block order and budgets

| # | Block | Budget | Job |
|---|---|---|---|
| 1 | Lead hook | 1 line, ≤ 12 words | Stand alone. Many shoppers read nothing else |
| 2 | Intro | 2–3 sentences, 25–50 words | Name the transformation and who it is for |
| 3 | Benefit bullets | 3–5, each ≤ 16 words | One benefit each, payoff front-loaded |
| 4 | Good to know | 2–4 lines, ≤ 60 words | Remaining objections, one per line |
| 5 | CTA | 1 line | Restate the benefit, then the action |
| 6 | Details / Specs | unlimited, literal | Every number, dimension, material, care step |

Total sell copy (blocks 1–3 and 5 — hook, intro, bullets, CTA): **80–160 words.** Past that, the page is being read by nobody. The Good to know block sits outside that budget, at 2–4 lines and ≤ 60 words.

## Why this order

The hook earns the next two lines. The intro earns the bullets. The bullets earn the Details block. Anyone who reaches Details is a spec-hunter doing final verification — they want density and completeness, and they want it *out of the way* of the sell.

## Block rules

### 1. Lead hook
- Must work with zero context above it.
- Banned openers: "Premium quality", "High-quality", "Introducing", "Welcome to", "The ultimate", "Say hello to", "Meet the".
- Banned shape: the product category as a noun phrase ("A premium LED desk lamp").
- Good shapes: the transformation ("Slices a ripe tomato without crushing it"), the enemy ("No rust, no smell, no scrubbing"), the moment ("Out of the box and on your desk in three minutes").

### 2. Intro
- Sentence 1: the transformation or the enemy.
- Sentence 2: the mechanism (the one spec doing the work).
- Sentence 3 (optional): who it is for, and who it is not for.
- No bullet formatting here, even if it feels punchier.

### 3. Benefit bullets
- **Payoff first.** First 2–4 words bold, then the spec as proof.
- Order: strongest differentiator first, table-stakes last. The first bullet carries most of the load.
- **3 bullets** when the product has one dominant differentiator. **5** when it has several comparable ones. Never pad to 5.
- Avoid stacking bullets that all trace to the same spec.
- Every bullet answers a real doubt or delivers a real outcome. A bullet that only restates a dimension is a Details line.

### 4. Good to know
- Reformats objections into reassurance, one line each.
- Introduce as "Good to know" or a short "Details"-free heading. Not "FAQ".
- Put the inconvenient truths here — the ones that prevent a return rather than a sale.

### 5. CTA
- Restate the benefit, then the action: "Ships with a 5-year warranty — add it to your cart."
- Bare "Buy now", "Shop now", "Add to cart", "Order today" alone fails the delivery check.
- No fabricated urgency. See the compliance doc.

### 6. Details / Specs
- Literal transcription. No adjectives, no benefit wrapping.
- Cover: dimensions (and folded / assembled / with-handle variants), weight, materials, capacity, power/compatibility, certifications, what's in the box, care instructions, warranty, country of manufacture if the source has it.
- Use a definition-list shape (`Label: value`) — it survives copy-paste into any CMS.

## Handling a 40-row spec sheet

Cluster into 5–7 groups: Dimensions · Materials · Compatibility · Power · In the box · Care · Warranty. Then:

1. Route each row through the bridge test (`benefit-translation.md`).
2. Rows that pass → bullets or Good to know.
3. Everything else → Details, grouped, unfiltered.
4. Never delete a row because it is unflattering; relocate it.

## Mobile-first constraints

- Assume a 360 px viewport. A bullet over ~16 words wraps to three lines and stops being scanned.
- No paragraph over 3 lines.
- Never rely on bolding alone to carry meaning — the payoff word must also be the first word.
- Tables inside Details are acceptable; tables inside the sell blocks are not.

## SEO note

- The hook should contain the primary keyword **naturally**, once. Keyword stuffing is a conversion tax.
- Put secondary and long-tail terms in the Details block, where density is expected.
- The H1 is usually the product name from the catalogue, not the hook — confirm before replacing it.
