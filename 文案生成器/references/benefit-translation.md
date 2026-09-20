# Spec → Benefit Translation

The whole job of this skill in one rule: **no spec ships naked.** Every surviving spec must complete the bridge.

```
<feature>, which means <consequence the buyer experiences>
```

Spec count is not value. A nine-row spec sheet that yields four real benefits beats a nine-row spec sheet pasted into a bullet list.

## The bridge test

Run every candidate feature through three questions:

1. **So what?** Does it change an outcome the buyer actually experiences, or does it only describe the object?
2. **Compared to what?** What is the default / cheap alternative, and is the difference perceptible?
3. **Who cares?** Which of the target customer's jobs, pains, or moments does this touch?

Scoring:

| Answers | Action |
|---|---|
| 3 × yes | Lead with it — candidate for the hook or bullet #1 |
| 2 × yes | Keep it as a bullet |
| 1 × yes | Demote to the Details block; strip the adjective |
| 0 × yes | **Drop it** and log the drop in the delivery notes |

Two questions can honestly be "unknown" — that is a signal to ask the user, not to invent an answer.

## Translation table by spec family

| Spec family | Raw form | Bridge | Payoff vocabulary |
|---|---|---|---|
| Alloy / metal | 316 stainless steel | which means → names the failure it prevents | won't rust, won't pit, won't flake, no metallic taste |
| Textile | 100% organic cotton | which means → skin or laundering effect | breathes, doesn't itch, survives 50 washes |
| Dimension | 12 in / 30 cm | which means → the fit scenario | fits in a, slides under b, hangs past c |
| Capacity | 1.7 L | which means → what it holds | holds four servings, a full workday of water |
| Weight | 280 g | which means → the carry experience | disappears in a pocket, no shoulder ache |
| Power | 60 W | which means → the task it finishes | clears a room, boils in 4 minutes |
| Runtime | 9 h | which means → the trip it survives | lasts the flight, gets through a shift |
| Speed | 0.4 s | which means → perception | you stop noticing the wait |
| Battery | 5000 mAh | which means → days between charges | three days normal use |
| Water resistance | IPX7 | which means → the scenario, **and the limit** | survives the sink, not the pool |
| Certification | NSF / FDA / CE | which means → someone else already checked | third-party verified, not self-declared |
| Warranty | 5-year | which means → risk transfer | you're not buying this twice |
| Assembly | tool-free, 4 steps | which means → friction removed | out of the box in three minutes |
| Care | machine wash cold | which means → the ongoing cost | no dry-cleaning tax |
| Compatibility | fits M1–M4 | which means → the buyer's own device | check yours against one line |
| Noise | 42 dB | which means → the room it lives in | quieter than a fridge |
| Sourcing | single-origin | which means → taste or story | tastes like a place, not a blend |
| Ingredient | 15% vitamin C | which means → what the buyer sees | (careful: see compliance — no medical claims) |
| Material absence | BPA-free, PFAS-free | which means → the worry it removes | no plastic aftertaste |

## Fix these, don't ship them

| Vague input | Why it fails | Rewrite pattern |
|---|---|---|
| "Durable construction" | no failure named | name the failure and the source number if there is one |
| "Premium materials" | category claim, zero information | name the material and one consequence |
| "Easy to use" | every competitor says it | count the steps, the parts, the minutes |
| "Versatile" | means nothing without a second use case | name two concrete contexts |
| "Lightweight" | relative | give grams and a comparison |
| "Ergonomic" | jargon | describe the body contact point |
| "High performance" | unfalsifiable | give the measured unit |
| "Eco-friendly" | unsubstantiated (see compliance) | name the specific attribute: recycled, refillable, FSC |
| "Designed for everyone" | nobody is everyone | name the one person it's for |

## Numbers discipline

- **Only source numbers.** Never average, round flatteringly, or interpolate. If the source says "up to 9 hours," write 9 — not 10.
- If the source gives a range, quote the range.
- If the source gives a lab condition ("600 ml under continuous use"), keep the condition; dropping it turns a fact into a claim.
- A number that appears in the body but not in the source fails the delivery check. `scripts/spec_coverage.py` reports these as invented.

## Payoff-front-loading

The bullet's first 2–4 words carry the payoff; the spec follows as proof.

- ✅ **No rust, ever.**  316 stainless steel, so a salt-air bathroom won't pit it.
- ❌ **316 stainless steel** — won't rust in a salt-air bathroom.

Order beats emphasis. Even when both facts appear, feature-first reads as a datasheet and payoff-first reads as a reason to buy.

## Where each spec goes

| Bridge strength | Destination |
|---|---|
| Carries the transformation | Lead hook |
| Strong, distinct | Benefit bullet (3–5 max) |
| Real but secondary | "Good to know" |
| Literal / needed by a spec-hunter | Details block only |
| Zero buyer outcome | Dropped, and logged |
