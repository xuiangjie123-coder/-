# Worked Examples

Three inputs of decreasing quality, to show the input → output shape and the delivery notes that ride along.

---

## Example 1 — A real spec sheet (best case)

**Input:** raw spec sheet, DTC kitchen brand, no voice brief.

```
Product: 8" chef's knife
Blade: Japanese AUS-10 high-carbon stainless, 61 HRC
Construction: 67-layer Damascus cladding
Grind: 15° per side
Handle: black pakkawood, full tang
Weight: 8.1 oz
Balance point: at the bolster
Hardness test: holds edge through 200 lb of cardboard
Care: hand wash, dry immediately
Warranty: lifetime
Origin: Japan (Seki City)
```

**Voice inferred:** Plain-Spoken Expert / Quiet Premium blend. Assumption stated in the notes.

**Output:**

> **The knife you stop thinking about.**
>
> Most kitchen knives go dull in six months, then fight the tomato. This one is ground to 15° per side and hardened to 61 HRC. It is balanced at the bolster, so the weight sits in your hand, not the blade.
>
> - **Cuts clean.**  A 15° edge slices a ripe tomato instead of squashing it.
> - **Stays sharp for years.**  AUS-10 carbon steel at 61 HRC, tested through 200 lb of cardboard.
> - **Sits light in hand.**  8.1 oz, balanced at the bolster, so the blade works.
> - **Lasts a lifetime.**  Full-tang pakkawood handle, backed by a lifetime warranty.
>
> Good to know
> - Hand wash and dry right away — carbon steel will spot if it sits wet.
> - The Damascus pattern is forged, so each knife looks a little different from the photo.
> - 15° is a shallower angle than most Western knives; if you use a steel, use light strokes.
>
> A knife you buy once — add it to your cart with the lifetime warranty in place.
>
> **Details**
> Blade: 8 in / 20.3 cm, AUS-10 high-carbon stainless, 61 HRC
> Construction: 67-layer Damascus cladding, full tang
> Edge: 15° per side
> Handle: black pakkawood
> Weight: 8.1 oz / 230 g
> Balance: at the bolster
> Hardness test: holds an edge through 200 lb of cardboard
> Origin: Seki City, Japan
> Care: hand wash, dry immediately
> Warranty: lifetime

This exact text is the package's regression fixture (`scripts/tests/draft_knife_good.md` against `scripts/tests/spec_knife.txt`). It passes `validate_pdp.py` with 0 errors and 0 warnings, and `spec_coverage.py` with 0 missing and 0 body-only atoms — use it as the shape reference.

**Dropped / regrouped specs**

| Spec | Disposition | Reason |
|---|---|---|
| 67-layer Damascus | Details only | visually distinctive, zero functional consequence — the pattern line in Good to know covers the perception |
| Full tang | Bullet #4 (as proof) | real durability signal |
| Hardness test | Details only | the test is the proof for bullet #2; restating it in the sell would be a datasheet |
| Origin: Seki City | Details | provenance aids trust but is not a transformation |

**Unsupported claims:** none requested. "Stays sharp for years" rests on the 200 lb edge-holding test in the source, stated as the test rather than as an industry statistic.

---

## Example 2 — A spec list with objections

**Input:** mineral sunscreen, brand voice = Clinical Trust, target = sensitive-skin adults.

```
Product: mineral sunscreen SPF 50, 50 ml
Active: 21% zinc oxide, non-nano
Also: 5% niacinamide, squalane, no fragrance, no alcohol
Finish: untinted (also available tinted)
Water resistance: 80 min
Certification: reef-safe filter list confirmed
Testing: in-vitro SPF per ISO 24443
```

**Silent doubts** (from `objection-library.md`, beauty): white cast, greasiness, pilling under makeup, eye sting, "will it break me out", and the medical-line question — this is a cosmetic, so no treatment claims.

**Output:**

> **Zinc that does the job without the cast.**
>
> This mineral sunscreen is built for reactive skin. The filter is 21% non-nano zinc oxide, with no fragrance and no alcohol. It goes on as a lotion, not a paste.
>
> - **Protection without the mask.**  21% zinc oxide, untinted, dries down clear.
> - **Nothing to react to.**  No fragrance, no alcohol, no essential oils.
> - **No pilling under makeup.**  Squalane-based, applies as a lotion, waits 60 seconds before foundation.
> - **Won't sting your eyes.**  Mineral-only filter, no chemical absorbers.
>
> Good to know
> - On deeper skin tones the untinted version can leave a slight brightening cast — the tinted version avoids this.
> - Reapply every 2 hours, and after 80 minutes in water.
> - This is a cosmetic sunscreen. It reduces sun exposure; it does not treat or repair existing sun damage.
>
> Daily protection your skin won't argue with — add it to your cart.
>
> **Details**
> Size: 50 ml / 1.7 fl oz
> Active filter: 21% zinc oxide, non-nano
> Also contains: 5% niacinamide, squalane
> Free from: fragrance, alcohol, essential oils
> Finish: untinted (tinted version available separately)
> Water resistance: 80 minutes
> SPF testing: in-vitro, per ISO 24443
> Filter profile: confirmed against reef-restricted filter lists
> Use: apply generously 15 min before exposure; reapply every 2 h

**Dropped / regrouped specs**

| Spec | Disposition | Reason |
|---|---|---|
| ISO 24443 testing method | Details | credibility signal for spec-hunters; too technical for the sell |
| Tinted variant | Good to know | answers the cast doubt better than a bullet |
| 5% niacinamide | Intro | not a differentiator at this concentration; stated, not sold |

**Unsupported claims:** the input implied "heals sun damage" — declined and replaced with the cosmetic-scope line in Good to know. "Reef-safe" was reduced to the supportable phrasing (confirmed against restricted-filter lists) rather than the absolute term.

---

## Example 3 — A bare template description (worst case)

**Input:** literally this, nothing else.

```
High quality LED desk lamp. Premium materials, modern design, eye protection,
adjustable, USB powered. Perfect for home and office.
```

**What to do:** do not pad. Ask for the specific facts that decide the purchase — this is the "one detail competitors omit" moment.

**One follow-up:**

> I can write this, but five facts would double its power: the CRI or colour temperature, the actual brightness in lumens, the arm's reach and number of joints, whether the clamp is included, and the flicker rating. Send whatever exists — I'll write around what's missing rather than invent it.

**Assuming the answer is:** 3000–6000 K, CRI 95, 500 lumens max, two joints, clamp + base both included, flicker-free at all levels, USB-C 5 V/2 A, 3-year warranty.

**Output:**

> **Light that doesn't lie about the colour.**
>
> A CRI of 95 means the colours at your desk are the ones actually there. Cheap LEDs make reds and greens muddy. It runs flicker-free from a warm 3000 K to 6000 K for detailed work.
>
> - **Colours you can trust.**  CRI 95, so swatches and proofs match real light.
> - **No flicker, no headache.**  Flicker-free across the full dimming range.
> - **Reaches across the desk.**  Two joints, wide arc, clears a monitor.
> - **Clamps to any desk.**  Clamp and weighted base both included.
>
> Good to know
> - At 500 lumens it is a task light, not a room light — it will not light a bedroom.
> - Powered by USB-C at 5 V/2 A. A phone charger works; a laptop port may dim it at full output.
> - The clamp opens to 2 in / 5 cm — measure your desk edge first.
>
> A lamp that shows you the real colour — add it to your cart.
>
> **Details**
> Colour temperature: 3000–6000 K, adjustable
> CRI: 95
> Brightness: up to 500 lumens, dimmable
> Flicker: flicker-free across all levels
> Arm: two joints, adjustable arc
> Mounting: clamp (opens to 2 in / 5 cm) and weighted base included
> Power: USB-C, 5 V / 2 A
> Warranty: 3 years

**Dropped specs from the original input**

| Input phrase | Disposition | Reason |
|---|---|---|
| "High quality" | Dropped | category claim, no information — replaced by CRI and flicker facts |
| "Premium materials" | Dropped | no material was named; ask or omit |
| "Modern design" | Dropped | subjective, untestable |
| "Eye protection" | Dropped | this is a health-adjacent claim (see compliance §3); replaced with the measurable "flicker-free" |
| "Perfect for home and office" | Replaced | "everyone" claims convince no one; replaced with a limitation and a real mounting fact |

**Unsupported claims:** "eye protection" refused — an eye-health claim needs the relevant standard and testing; flicker-free is the supportable substitute. "Perfect for home and office" deleted rather than rewritten, since it carries no information.
