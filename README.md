[README.md](https://github.com/user-attachments/files/32431760/README.md)
# 文案生成器 · Product Description Writer

> Turns a raw spec sheet into an on-site PDP master copy — benefit-led, scannable, in the brand's voice.

把产品规格表翻译成能转化的**站内详情页(PDP)主文案**。方法只有两条:**强制把规格翻译成买家利益**,**诚实回答买家的隐性异议**。

## 它做什么

输入一份规格清单——脏的、乱的、截图 OCR 出来的都行。输出一整块可直接粘贴的主文案:

```
钩子行 → 2–3 句引言 → 3–5 条利益 bullet → 异议处理(Good to know)
      → 利益重述式 CTA → 完整规格块
```

并附带两份机器校验报告,以及**被丢弃的规格**和**无法支撑的 claim** 清单。

## 什么时候用 / 不用

| | |
|---|---|
| ✅ 用 | 单个产品的站内 PDP 主文案;手上有规格表、卖点 bullet 或干巴巴的模板描述 |
| ❌ 不用 | Amazon / 第三方平台 listing → 用 `amazon-listing-optimizer` |
| ❌ 不用 | 把一份主文案扩写成多尺码、多颜色变体 → 用 `variant-copy-scaler` |

## 工作流

1. **收集输入** — 填 `assets/intake-brief.md`。调性未知就按类目推断,**只问一个**校准问题;规格太薄就追问竞品没写的那个细节,不堆废话。
2. **找到唯一的购买理由** — 写核心转变,不是品类名("切开熟番茄而不压烂它",不是"刀")。
3. **每个规格翻译成利益** — 固定句式:规格 + which means + 利益。**翻译不出买家在意的利益,就把这个 feature 删掉并登记。**
4. **主动提出并回应异议** — 按品类清单点名没说出口的疑虑(尺码、耐用、退货、"适合我吗"),每条一句安抚;偏小就直说偏小。
5. **按 F 型浏览排版** — 严格按 `assets/pdp-master-template.md` 的区块顺序与字数预算填。
6. **校准语气** — 六个品牌原型选一个,结果记进 `assets/voice-card.md`。
7. **检查 claim** — 性能、对比、健康、安全、环保、紧迫感类说法,一律先过 `references/compliance-and-claims.md`。
8. **交付前校验** — 跑下面两个脚本。错误必须全清;**警告要么改掉,要么在备注里解释**。

## 目录结构

```
├── SKILL.md                        工作流、质量标准、交付物、禁令
├── assets/
│   ├── intake-brief.md             信息采集表(动笔前必填)
│   ├── pdp-master-template.md      粘贴即用骨架 + 区块预算表
│   └── voice-card.md               一页品牌语气卡
├── references/
│   ├── benefit-translation.md      规格→利益的 bridge 三问 + 翻译对照表
│   ├── objection-library.md        通用九疑 + 8 个品类的具体异议与应答
│   ├── voice-calibration.md        五个语气旋钮 + 6 个品牌原型 + 单题校准话术
│   ├── pdp-anatomy.md              区块预算 + F 型排版 + 移动端与 SEO 约束
│   ├── compliance-and-claims.md    claim 举证表 + 中国广告法绝对化用语替换表
│   └── worked-examples.md          3 个由易到难的完整范例
└── scripts/
    ├── spec_coverage.py            规格覆盖率检查
    ├── validate_pdp.py             文案质检
    └── tests/                      回归样本(1 好 + 1 坏,附规格表)
```

## 脚本

只用 Python 标准库,无第三方依赖。

```bash
# 规格覆盖率:证明源规格表每一项都有落点
python scripts/spec_coverage.py specs.txt draft.md

# 文案质检:结构、句长、违禁开头、风险 claim
python scripts/validate_pdp.py draft.md
```

| 开关 | 作用 |
|---|---|
| `--strict` | 警告也当失败(两个脚本都支持) |
| `--json` | 输出机器可读 JSON |
| `--allow-missing 67层` | 声明某个规格是有意丢弃的,不计入 MISSING |
| `-` | 从 stdin 读草稿,方便管道 |

默认预算(中英双语自动切换):

| 区块 | 英文 | 中文 |
|---|---|---|
| 钩子 | ≤12 词 | ≤24 字 |
| 利益 bullet | 3–5 条 × ≤16 词 | 3–5 条 × ≤32 字 |
| 加粗卖点词 | 2–4 词 | **≤4 字** |
| 单句 | ≤20 词 | ≤40 字 |
| sell 总量(钩子+引言+bullet+CTA) | 80–160 词 | 120–320 字 |
| Good to know | ≤60 词 | ≤120 字 |

预算全部可用命令行覆盖(如 `--bold-max-cjk`、`--max-sell-cjk`)。

## 硬性禁令

- 不编造性能数字、认证、材质、健康/安全/收益类 claim
- 不用 "premium quality" 或任何泛泛的品类套话开头
- 不伪造稀缺、倒计时、低库存 —— 只有真实时才用紧迫感
- 不保留翻译不出买家利益的 feature
- 不用光秃的 "Buy now" 收尾 —— CTA 里要重述利益
- **不删除不体面的规格** —— 移到规格块,或在 Good to know 里说明**不适合谁**

## 已验证

```
好样本  scripts/tests/draft_knife_good.md
  validate_pdp.py   → 0 error / 0 warn        (Flesch 89.3,均句 12.6 词)
  spec_coverage.py  → 20 个原子全部 OK_DETAILS, --strict 也通过

坏样本  scripts/tests/draft_knife_bad.md
  validate_pdp.py   → 6 error / 18 warn
                      命中:钩子禁语、缺卖点前置、bare CTA、缺规格块、
                            虚假紧迫感、需举证的 claim
```

两个脚本都不依赖标记,粘贴即用的裸文案能直接校验。

## 来源与改动

- 上游:`SkillMedev/skills` 仓库的 `skills/product-description-writer`,原包**只有 `SKILL.md`**
- 本仓库补上 `references/`(6 篇)、`scripts/`(2 个可运行脚本 + 回归样本)、`assets/`(3 个模板)
- `SKILL.md` 的 frontmatter 与原有 6 条 Do NOT 契约保持上游原样;工作流由 6 步扩到 8 步,以接入上述附属文件
- 尚未指定开源许可证
