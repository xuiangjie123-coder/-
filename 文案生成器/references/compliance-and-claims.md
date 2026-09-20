# Compliance and Claims

The skill's hard boundary: **write only what the source can support.** This file is the check to run before any performance, comparative, health, safety, environmental, or urgency claim ships.

This is practitioner guidance, not legal advice. Where a claim is regulated, route it to the brand's legal reviewer with the source cited.

## 1. Every claim needs a source

| Claim type | Example | Required support |
|---|---|---|
| Performance number | "lasts 9 hours" | Tested figure in the source, with its condition |
| Comparative | "quieter than a fridge" | Both measurements, or the comparison removed |
| Superlative | "the strongest", "best" | Nothing supports this category — rewrite or delete |
| Certification | "NSF certified" | Certificate number or issuing body in the source |
| Material / composition | "316 stainless" | Bill of materials |
| Health / safety | "safe for babies" | Standard tested against, named |
| Environmental | "biodegradable", "carbon neutral" | Specific standard, scope, and timeframe |
| Earnings / outcomes | "saves you $200 a year" | Calculation shown, or delete |
| Testimonial | "customers say it changed…" | A real, permissioned, attributable quote |

**No source, no claim.** Ask the user for the fact. Never soften an unsourced claim into vagueness — vagueness is still a claim, and it is a weaker one.

## 2. Absolute-language prohibition (China market, 广告法)

Chinese advertising law prohibits absolute terms. Strip these on sight, even when the source contains them:

| Banned | Compliant substitute |
|---|---|
| 最（最好/最优/最强/最便宜） | 更 / 较 / 在…测试中 |
| 第一 / 唯一 / 独家 | 首批 / 少数 / — |
| 国家级 / 世界级 / 顶级 | 通过 XX 认证 / — |
| 100% / 彻底 / 完全 | 经测试为 XX% / 大幅 |
| 永久 / 终身（无依据时） | 产品有效期 / 质保期内 |
| 根治 / 特效 / 药到病除 | 辅助 / 有助于（且需按品类资质） |
| 全网最低价 / 秒杀全网 | 限时价（需真实比价依据） |
| 无任何副作用 | — （删除，不可替换） |

`scripts/validate_pdp.py` flags the highest-precision subset of this table when CJK is present — treat every row above as the rule, not just the flagged ones.

## 3. Health, beauty, and safety hard lines

- **Cosmetics (China 化妆品监督管理条例 / US FDA cosmetic rules).** Cosmetic copy may describe appearance and sensory attributes. It may **not** claim to treat, cure, prevent, or repair a disease or a physiological function. "Removes wrinkles" fails; "visibly smooths the look of fine lines" is a cosmetic appearance claim — and only if the source supports it.
- **Supplements / food.** No disease claims, ever. Nutrient-content claims require the levels to be met and stated. Allergen statements must be transcribed from the source, never inferred.
- **Dermatology-adjacent language.** "Dermatologist tested" requires the test; "dermatologist recommended" requires the survey. "Hypoallergenic" is a claim, not a fact.
- **Children's and baby products.** Safety statements only from the source, with the standard named. No "no choking hazard" phrasing of any kind.
- **Devices.** Never imply a medical purpose without the relevant registration. Distinguish "relief" (regulated) from "comfort" (not).

## 4. Environmental claims

Vague green language is a regulated claim in most major markets now.

- ❌ "eco-friendly", "sustainable", "green", "planet-positive" — vague, delete.
- ✅ Name the attribute and its reference: "35% post-consumer recycled PET", "refillable: one pouch replaces three bottles", "FSC-certified carton".
- Carbon claims need scope + methodology + offset vs reduction distinction.
- "Biodegradable" needs the environment and the timeframe.

## 5. Urgency claims

Urgency is allowed **only when it is true and verifiable**:

| Allowed if verifiable | Always banned |
|---|---|
| A real batch size ("first batch of 400") | Countdown timers that reset |
| A real end date | "Ends tonight!" with no end |
| A real stock figure from the system | "Only 3 left!" invented |
| A real seasonal window | "Selling fast" without data |

Every urgency line must cite its source in the delivery notes. If it cannot be cited, it does not ship — no exceptions.

## 6. Refusal and substitution patterns

When asked to write a claim the source cannot support, refuse the claim and offer the compliant rewrite. Do not refuse the whole task.

| Requested | Response pattern |
|---|---|
| "Say it cures acne" | Decline. Offer: "Describe only what the formula is and how it feels, plus any appearance claim actually tested." |
| "Put 'best in class'" | Decline. Offer: "Replace with the specific measured advantage, or with the comparison the data supports." |
| "Add 'only 5 left'" | Decline unless stock data is provided. Offer the real batch or date if one exists. |
| "Say it's FDA approved" | Only if the registration is in the source. Otherwise: "registered/listed with" only if literally true, otherwise drop. |
| "Claim it's 100% natural" | Decline the absolute. Offer the actual composition from the source. |
| "Say customers lost 10 lb" | Decline. Earnings/outcome claims need substantiation and typically regulated approval. |

Script to use, briefly and without lecturing:

> I can't write "<claim>" — there's nothing in the source to support it, and it's a claim type that gets challenged. Here's the closest compliant line: "<rewrite>". If you have the test report or certificate, send it and I'll write the strong version.

## 7. Delivery-notes requirement

Every delivery ends with two lists, and this is part of the deliverable, not a courtesy:

1. **Dropped specs** — what was removed and the bridge-test reason.
2. **Unsupported claims** — what was requested or implied but could not be written, plus the compliant substitute used.
