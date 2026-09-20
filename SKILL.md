---
name: Product Description Writer
description: Writes the single on-site PDP master copy - a benefit-led, scannable product detail page in the brand's voice - from a raw spec sheet or feature list. Use when you have a spec list, feature bullets, or a bare template description for one product and need conversion copy for its on-site product detail page. Do NOT use for Amazon or marketplace listings - use amazon-listing-optimizer instead; do NOT use to spin one master into many size/color variants - use variant-copy-scaler instead.
---
# Product Description Writer

Translate a product's specs into the on-site PDP master copy: benefit-led, scannable, in the brand's voice, decidable in eight seconds on a phone.

## Bundled files

Load only what the job needs.

| File | Load when |
|---|---|
| `assets/intake-brief.md` | Always, first. Fill it before writing a word. |
| `assets/pdp-master-template.md` | Always. The paste-ready skeleton and the block budgets. |
| `references/pdp-anatomy.md` | Deciding block order, bullet count, bolding, mobile limits. |
| `references/benefit-translation.md` | Translating the spec sheet; also the bridge test for dropping a feature. |
| `references/objection-library.md` | Surfacing the silent doubts for this category. |
| `references/voice-calibration.md` | Brand voice is unknown, or you need the single calibrating question. |
| `references/compliance-and-claims.md` | Any claim about performance, health, safety, environment, or urgency. Read before writing the CTA. |
| `references/worked-examples.md` | You want the input → output shape on three inputs of decreasing quality. |
| `assets/voice-card.md` | Once voice is settled, record it so it stays consistent. |
| `scripts/spec_coverage.py` | Before delivering. Proves every source spec is covered or explicitly logged as dropped. |
| `scripts/validate_pdp.py` | Before delivering. Lints structure, sentence length, banned openers, risky claims. |

## Workflow

1. Gather inputs. Open `assets/intake-brief.md` and fill it: the spec/feature list, the target customer, the brand voice. If voice is unknown, infer it from the category with `references/voice-calibration.md` and ask exactly one calibrating question. If the spec list is thin, ask for the one detail competitors omit - do not pad with fluff.
2. Find the one reason they buy. Name the core transformation or job-to-be-done, not the product category ("slices a ripe tomato without crushing it," not "knife"). This is the lead hook. Mind the hook budget in `assets/pdp-master-template.md`.
3. Translate each spec to a benefit. Use the bridge in `references/benefit-translation.md`: feature + "which means" + benefit ("316 stainless steel, which means it won't rust in a salt-air bathroom"). Keep the spec for credibility, the benefit for desire. Drop any feature that fails the bridge test, and log the drop.
4. Surface and answer objections. Work the category list in `references/objection-library.md`. Name the silent doubt - sizing, fit, durability, returns, "will this work for me" - and give one reassuring line each, woven into bullets or a short "Good to know" note. If it runs small, say so.
5. Assemble for the F-pattern scan. Fill `assets/pdp-master-template.md` in its given order: lead hook, 2-3 sentence intro, 3-5 benefit bullets with the payoff word front-loaded and the first 2-4 words bold, a benefit-restating CTA, then a "Details" or "Specs" block for literal numbers, dimensions, materials, and care.
6. Calibrate voice. Match sentence length, vocabulary, and warmth to the brand (premium skincare is calm and precise; a snack brand is playful). Record the result on `assets/voice-card.md`.
7. Check the claims. Run every performance, comparative, health, safety, environmental, and urgency claim past `references/compliance-and-claims.md`. An unsupported claim gets refused, with the compliant alternative offered in its place.
8. Validate before delivering. Run `scripts/spec_coverage.py <spec> <draft>` to prove coverage or produce the drop list, then `scripts/validate_pdp.py <draft>` to catch structure, sentence-length, and claim problems. Fix every error; read every warning and either fix it or explain it in the notes.

## Quality bar

- The first line works as a standalone hook - many shoppers read nothing else.
- Every benefit traces to a spec in the source; every spec that survives earns its place.
- Sentences stay under 20 words; bullets front-load the payoff.
- Spec-hunters can find every literal number in the Details block without it cluttering the sell.
- Every objection a buyer would have before adding to cart is answered honestly.
- Both scripts run clean, or every remaining finding is explained.

## Deliverable

Produce the complete PDP master copy as one paste-ready block: lead hook line, 2-3 sentence intro, 3-5 benefit bullets (payoff front-loaded, opening words bold), objection-handling lines or a "Good to know" note, a benefit-restating CTA, and the Details/Specs block with every literal number, dimension, material, and care instruction from the source. Flag any spec you dropped and why, and any claim you could not support from the inputs.

Append the two machine-checked lists: the `spec_coverage.py` verdict (missing / body-only / acknowledged atoms, plus any number in the copy with no source) and the `validate_pdp.py` summary (errors, warnings, notes). These are part of the deliverable, not an afterthought.

## Do NOT

- Do not invent performance numbers, certifications, materials, or health/safety/earnings claims. Use only what the source provides; if asked to claim an outcome the source doesn't support, refuse and offer a compliant alternative.
- Do not open with "premium quality" or any generic category claim.
- Do not fabricate scarcity, countdowns, or low-stock urgency. Use urgency only when it is true (limited batch, seasonal, real low stock).
- Do not keep features that translate to no buyer benefit.
- Do not end with a bare "Buy now" - restate the benefit in the CTA.
- Do not delete an unflattering spec. Relocate it to the Details block, or state it in "Good to know" and say who the product is not for.
