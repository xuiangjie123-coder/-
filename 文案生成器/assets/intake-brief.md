# Intake Brief

Fill this before writing a word. Anything left blank becomes a stated assumption in the delivery notes — never a silent invention.

---

## 1. Product

- **Product name (catalogue H1):**
- **Category:**
- **Price point:** (sets the value framing)
- **Market / channel:** on-site PDP · region:
- **Variant this copy is for:** (size, colour, model)

## 2. Spec / feature sheet

Paste raw. Do not clean it up first — the messier it is, the more useful the extraction.

```
<paste here>
```

- [ ] Every value is copied, not paraphrased
- [ ] Units are as written in the source
- [ ] I have flagged any row that is a marketing claim rather than a spec

## 3. Target customer

- **Who is this for, in one sentence:**
- **The job they are hiring it for:**
- **What they use today instead:**
- **What they are afraid of before adding to cart:**
- **Who this is NOT for:** (lets the copy say so, which converts better than a refund)

## 4. Brand voice

- **Their four words:** (e.g. "calm, precise, a little reserved")
- **Archetype** (pick one, see `references/voice-calibration.md`):
  Quiet Premium · Warm Everyday · Bright Playful · Plain-Spoken Expert · Clinical Trust · Design-Led Minimal
- **Sentence-length target:**
- **Words we always use:**
- **Words we never use:**
- **The one calibrating question asked / answer given:**
- [ ] Voice card filled in (`assets/voice-card.md`)

## 5. Claims and compliance

- **Certifications available with numbers:** (do not list one you cannot produce)
- **Test reports available:** (which figure, tested how)
- **Health / safety / environmental language permitted by the brand:**
- **Claims legal has already approved:**
- **Urgency facts that are true:** (batch size, end date, real stock)
- [ ] `references/compliance-and-claims.md` read before writing the CTA
- [ ] Region-specific absolute-language rules checked (CN market: advertising law)

## 6. Known objections

- **Top three doubts buyers raise:**
  1.
  2.
  3.
- **Return reasons from support, if available:**
- **The unflattering truth we will state honestly:** (runs small, needs two people, loud, etc.)

## 7. Constraints

- **Word budget:**
- **SEO primary keyword:** (used once, naturally, in the hook)
- **Secondary terms for the Details block:**
- **Platform field limits:** (short description, bullet cap, character caps)
- **Deliverable format:** plain paste-ready block / CMS fields / markdown

---

## Before delivery

- [ ] `scripts/spec_coverage.py` run against the source sheet
- [ ] `scripts/validate_pdp.py` run against the draft
- [ ] Every dropped spec logged with its bridge-test reason
- [ ] Every unsupported claim logged with the compliant substitute used
