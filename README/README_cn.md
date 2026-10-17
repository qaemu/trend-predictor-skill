<div align="center">

<img alt="TREND-PREDICTOR：把项目所依赖的约束条件向前推演 5 年和 10 年，看它何时变得可行" src="../assets/banner.svg" width="100%">

<br>

**一个智能体技能（Agent Skill）：把项目所依赖的约束条件向前推演 5 年和 10 年，<br>告诉你项目可行的概率有多大、什么会拖住它，以及何时该开始动手。**

[English](../README.md) | [Español](README_es.md) | **简体中文**

[![License: MIT](https://img.shields.io/badge/license-MIT-2F6FB5?style=flat-square&labelColor=111111)](../LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-8DB8E3?style=flat-square&labelColor=111111)](../skills/trend-predictor/scripts/trend_predictor.py)

[快速开始](#快速开始) · [工作原理](#工作原理) · [测试](#效果如何) · [安装](#安装) · [用法](#用法) · [局限](#局限) · [常见问题](#常见问题)

</div>

---

## 快速开始

```bash
npx skills add qaemu/trend-predictor-skill
```

也可以在 Claude Code 中通过插件市场手动添加：

```text
/plugin marketplace add qaemu/trend-predictor-skill
/plugin install trend-predictor@trend-predictor
```

> [!NOTE]
> TREND-PREDICTOR 给出的是概率，不是预言。每个结果都是有条件的（"*如果* 2010–2025 年的趋势延续，到 2035 年有 61% 的可能"），并写成带日期、日后可以核对的判断。

## 与 PARADIGMA 搭配效果最好

TREND-PREDICTOR 是一对工具中向前看的那一半。[**PARADIGMA**](https://github.com/qaemu/paradigma-skill) 向后看：一个领域里哪些约束在过去几年下降了、谁在利用每一项变化、哪里还有空白。TREND-PREDICTOR 向前看：随着这些约束继续变化，某个具体项目会不会变得可行？

**建议同时安装 PARADIGMA。** 先在你的领域上运行它，再在你正在考虑的项目上运行 TREND-PREDICTOR：

```bash
npx skills add qaemu/paradigma-skill
```

- 两者使用相同的数据文件（`points.csv`、`constraints.csv`、`noncost.csv`），因此一次 PARADIGMA 运行就是现成的起点：TREND-PREDICTOR 直接复用其带来源的数据，不必重新收集。
- PARADIGMA（v0.4.2 及以后）会把找到的较早数据点保存在 `out_of_window.csv` 中。预测需要 10 年以上的历史，这些较早的数据在这里很有用。
- PARADIGMA 告诉你**哪些**约束重要；TREND-PREDICTOR 只为项目所依赖的 3–5 条曲线收集更密的历史数据。

## 为什么要预测约束

当一个项目所依赖的东西足够便宜、足够好、并且被允许时，它就是可行的：执行器低于目标成本、电池高于目标能量密度、某项法规已经生效、某项专利已经到期。这些东西沿着可测量的趋势变化，而关于技术预测的研究对什么方法有效已有明确结论：

- **把一项技术自身的历史趋势，加上诚实的误差范围向前延伸，在约 10 年内的成本和性能预测上胜过专家小组**（[Farmer & Lafond 2016](https://arxiv.org/abs/1502.05274)；[Meng et al. 2021](https://www.cmcc.it/article/recent-technology-cost-forecasts-underestimate-the-pace-of-technological-change)）。专家和大型机构模型一贯过于悲观：模型预计 2010–2020 年太阳能成本每年下降 2.6%，实际约为 15%。
- **公告会夸大。** 宣布的 2030 年氢能产能中，只有约 11% 已做出最终投资决定（IEA，2025）。
- **太早和错了看起来是一样的。** 知道一项约束*何时*会越过你的门槛，和知道它*是否*会越过同样重要。

| 它是 | 它不是 |
|---|---|
| 用代码算出的、按需求和时间跨度给出的概率 | 用文字写出来的猜测 |
| 先在每条序列自己的历史上检验过的范围 | 向未来画出的直线 |
| 明确标出哪些数字是经验假设 | 自称拥有它并不具备的精度 |
| 一份带日期、可核对的预测清单 | 一次性的意见 |

## 工作原理

<img alt="八个步骤：需求、历史、回测、预测、定期事件、成熟度、评分、核查与报告" src="../assets/pipeline.svg" width="100%">

| 步骤 | 做什么 |
|---|---|
| **1. 需求** | 把项目拆成必须成立的条件：由单位经济推导出的成本或性能**目标**、带日期的**事件**（法律、专利到期、工厂）、**成熟度**步骤（TRL），以及由群体预测或公开调查支持的**判断**项。指出最近发生变化的约束，否则标出"太早"的风险。 |
| **2. 历史** | 辅助智能体为每条曲线收集 10 年以上的数据，每个数据点都有链接，每条序列只含一条产品线。若已有 PARADIGMA 数据则直接复用。 |
| **3. 回测** | 在信任一条序列之前，引擎从过去的每一年出发预测它，并检查现实落在其范围内的频率。 |
| **4. 预测** | 经过校准的范围（Farmer–Lafond 带漂移随机游走，Student-t 分布）。针对产品混杂、异常值、趋势变化和物理极限的自动修复，每一项都由明确的检验决定。仍然过于嘈杂的序列，会派一个智能体去找更密的数据。 |
| **5. 定期事件** | 有生效日期的法律、专利到期、标准、已宣布的工厂，每一项都按其状态（已宣布、已做最终投资决定、在建）打折扣。 |
| **6. 成熟度** | 有证据支持的技术成熟度步骤，以及来自 Metaculus、Manifold 或公开专家征询的判断输入。 |
| **7. 评分** | 每项需求在 +5 年和 +10 年内被满足的概率、联合概率与**最薄弱环节**并列、结论、敏感性分析、事前验尸，以及**启动窗口**：根据你的开发周期，应该在哪一年开始动手。 |
| **8. 核查 + 报告** | 一个没有参与研究的新智能体重新打开每个来源。输出报告、扇形图、工作簿，以及供日后评分的预测记录。 |

### 基本规则

1. **每个数字都有链接。** 缺失的数据报告为缺失，绝不估算。
2. **计算在代码中完成**（[`trend_predictor.py`](../skills/trend-predictor/scripts/trend_predictor.py)），绝不由模型估算。
3. **先在数据上检验方法。** 回测运行之前，任何序列都不被信任。
4. **最薄弱环节与联合概率并列报告。** 一个项目的表现不会好过它最差的需求。
5. **每个结果都写成带日期、可核对的预测**，以便之后的运行为之前的运行打分。

## 你会得到什么

<div align="center">
<img alt="可行性图：每项需求在 +5 年和 +10 年内被满足的概率、最薄弱环节和结论" src="../assets/feasibility.svg" width="78%">
<br>
<sub>可行性图示意。真实运行会为你项目的需求打分。</sub>
</div>

<br>

| 结论 | 规则 |
|---|---|
| **很可能可行** | 最薄弱需求 ≥ 80% 且联合概率 ≥ 60% |
| **有可能** | 联合概率 ≥ 35% |
| **希望渺茫** | 联合概率 ≥ 12% |
| **不太可能** | 联合概率 < 12% |
| **不确定** | 当最薄弱需求依赖薄弱证据时（C/D 级曲线，或由本次运行自己的智能体估计的概率），取代上述结论。原评分保留为"若输入成立" |

**交付物**

- **报告。** 先给出每个时间跨度的结论，以及最薄弱环节、启动窗口和最需要关注的一件事。然后是每项需求一张卡片（目标及其推导、扇形图、趋势、校准结果、已应用的修复、各时间跨度的概率）、带日期事件的时间线、成熟度、事前验尸、需要关注的信号和复查日期，最后是方法、置信度和来源。
- **工作簿（.xlsx）。** 打开即是 **Start here**，用通俗语言解释每个术语，之后是项目评分、每项需求的概率、各序列的拟合、预测范围、校准、事件、信号、预测记录，以及每个数据点及其链接。
- **图表。** 每条曲线一张扇形图（历史、预测中位数、50/80/95% 范围、目标、极限），外加可行性图。

## 效果如何

所有测试套件都可离线运行，其输出已提交到 [`tests/results/`](../tests/results/SUMMARY.md)。

| 套件 | 检验内容 | 结果 |
|---|---|---|
| [`test_engine`](../tests/results/test_engine.txt) | 在 60 项模拟技术上的校准；端到端的预测、可行性、图表和工作簿 | 13 / 13 |
| [`test_edge_cases`](../tests/results/test_edge_cases.txt) | 通胀、错误数据行、混合日期格式、缺口、物理极限、产品混杂、缺失文件、手动覆盖、"不确定"结论规则 | 39 / 39 |
| [`test_autofix`](../tests/results/test_autofix.txt) | 自动修复在干净数据上不添乱，在真实的趋势变化和异常值上有帮助 | 7 / 7 |
| [`test_real_data`](../tests/results/test_real_data.txt) | 在真实且有来源的数据上回测 | 12 / 12 |
| [`test_real_run`](../tests/results/test_real_run.txt) | 重新评分一次由免费模型（MiMo V2.6 Flash）完成的真实运行：概率完全复现，证据薄弱的结论变为"不确定" | 23 / 23 |

不加修饰地说，这些数字意味着：

- **校准。** 在模拟技术上，80% 范围包含了 77% 的结果，95% 范围包含了 93%。接近诚实，略窄。
- **修复。** 在干净数据上，只有 1–3% 的序列会触发，且不改变精度。在真实的放缓上，约一半情况会触发，并把预测误差降低 20–37%。当放缓被大量噪声掩盖时，大多不会触发，因为数据无法把它与偶然区分开。
- **真实数据**（[示例](../examples/backtest-predictive-maintenance)）：从 2013–2017 年出发的工资预测与实际情况相差约 3%。从 2019 年出发的预测在 2020–2023 年失准：先是新冠带来的跳升，然后是通胀压低了实际工资。80% 的范围本来就应该大约每 5 次失手 1 次，而且没有任何趋势模型能预见冲击。对于嘈杂的 GPU 发布价格，以及混杂了不同产品类型的热像仪序列，引擎正确地拒绝给出有信息量的 10 年预测，并要求更密的数据。

## 示例

**免费模型的一次真实运行。** [`examples/mimo-scan-swe-salaries`](../examples/mimo-scan-swe-salaries) 是 MiMo V2.6 Flash 在 OpenCode 中对美国软件工程薪资所做的完整扫描，附有评审。数据收集和核查站得住（84 项检查中 92% 一致）。三个项目结论中有两个依赖其自身智能体编出的概率，而且它引用的校准数字比自己文件中的更好。引擎现在会把这类结论标为"不确定"，指令也要求原样引用校准数字。

**一次回测。** [`examples/backtest-predictive-maintenance`](../examples/backtest-predictive-maintenance) 中是一次回测，使用的是 PARADIGMA 预测性维护示例中带来源的数据。它站在 2013、2015、2017 和 2019 年，仅用当时可得的数据进行预测，再与实际发生的情况比较。每个预测、范围和误差都在 `output/backtest.csv` 中。

## 安装

TREND-PREDICTOR 遵循开放的 [Agent Skills](https://agentskills.io) 格式：一个 `SKILL.md` 加一个 Python 引擎。任何能浏览网页、运行 Python，最好还能启动辅助智能体的智能体都可以使用它。

### 任意智能体（skills CLI）

```bash
npx skills add qaemu/trend-predictor-skill                    # 当前项目
npx skills add qaemu/trend-predictor-skill -g                 # 所有项目
npx skills add qaemu/trend-predictor-skill -a claude-code -a opencode
```

使用 [skills CLI](https://github.com/vercel-labs/skills)，支持 Claude Code、OpenCode、Codex、Cursor 等。用同样的方式添加 `qaemu/paradigma-skill`。

### Claude Code

作为插件安装，可通过 `/plugin` 获取更新：

```text
/plugin marketplace add qaemu/trend-predictor-skill
/plugin install trend-predictor@trend-predictor
```

插件技能带命名空间，所以运行方式是 `/trend-predictor:trend-predictor "<项目>"`。

或者作为个人技能安装，运行方式是 `/trend-predictor "<项目>"`：

```bash
git clone https://github.com/qaemu/trend-predictor-skill.git
mkdir -p ~/.claude/skills && cp -r trend-predictor-skill/skills/trend-predictor ~/.claude/skills/
```

### Claude 应用（网页、桌面、移动端）

1. 下载 [`dist/trend-predictor.zip`](../dist/trend-predictor.zip)。其中包含 `trend-predictor` 文件夹，内有 `SKILL.md` 和引擎。
2. 在 **Settings → Capabilities** 中打开 **Code execution and file creation**。
3. 进入 **Customize → Skills**，点击 **+**，再选择 **Create skill → Upload a skill**，选中该 ZIP 文件。

参见 Anthropic 指南：[Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)。

### OpenCode

```bash
git clone https://github.com/qaemu/trend-predictor-skill.git
mkdir -p ~/.config/opencode/skills && cp -r trend-predictor-skill/skills/trend-predictor ~/.config/opencode/skills/
```

OpenCode 也会读取 `~/.claude/skills/`，所以 Claude Code 的安装在那里同样可用。请先确认你的服务商支持网页搜索。没有它，技能无法收集数据。

### 依赖

| 需要 | 用途 |
|---|---|
| 网页搜索和页面抓取 | 每个数字都来自某个来源 |
| Python 3.10+，以及 `pandas`、`numpy`、`matplotlib`、`openpyxl`（推荐 `scipy`） | 引擎、图表和 Excel 工作簿。`scipy` 提供精确的 Student-t 范围 |
| 辅助智能体（可选） | 并行研究和独立核查。没有它们时，技能会一步一步运行，并把核查标记为自查 |

## 用法

```text
/trend-predictor "<项目>" [领域] [地区] [时间跨度] [standard|deep]
/trend-predictor scan "<领域>" [地区] [时间跨度]
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `项目` | 必填 | 交付什么、给谁、什么价格。如果太模糊而无法设定目标，技能会询问一次 |
| `scan` | — | 不针对单个项目：找出一个领域中最可能被越过的门槛，转化为 3–5 个候选项目并逐一评分 |
| `领域` | 自动推断 | 用于查找可复用的 PARADIGMA 运行 |
| `地区` | 全球 | 注明数据偏重美国或欧盟的地方 |
| `时间跨度` | `5,10` | 从最后一个完整年份起算的年数。允许 1–15；超过 10 年时输出的是情景，不是预测 |

```text
/trend-predictor "售价低于 2000 美元、能叠衣服的家用机器人" robotics global
/trend-predictor "面向小农户的太阳能冷库" agriculture "Latin America"
/trend-predictor scan "电网储能" global 5,10
```

> [!IMPORTANT]
> 一次完整运行会让多个智能体并行收集带来源的历史数据，消耗相当一部分套餐用量。请把它用于你认真考虑的想法，而不是头脑风暴。

## 用什么模型运行

关键在于对来源的严谨，以及在长时间运行中始终遵循流程。

| 角色 | 推荐 | 推理强度 |
|---|---|---|
| 主运行（需求、评分、报告） | Claude Opus 5.5 | 高 |
| 数据收集辅助 | Claude Sonnet 5.5 | 中–高 |
| 独立核查 | Opus 5.5 | 高 |

检验任意模型的方法：让它处理 3 条数据公开充分的曲线，例如锂离子电池包价格和太阳能组件价格，然后打开它返回的每个链接。**只要它编造了一个链接或一个数字，就不合格。**

## 数学原理

<details>
<summary><b>一条曲线如何被预测</b></summary>

<br>

1. **标准化。** 数值按单位性能表示，换算为不变价美元（FRED 的美国 CPI）。非美元数值需要附上有出处的汇率。
2. **年度值。** 每年数据点的中位数；当序列混杂多种产品时，改用截至当时可得的最佳值（价格-性能前沿）。
3. **拟合**（[Farmer & Lafond 2016](https://arxiv.org/abs/1502.05274)）。数值的对数是带漂移的随机游走：漂移 =（末值 − 首值）/ 年数；波动率 K 来自逐年变化，缺口按 √Δt 缩放。
4. **范围。** 中位数 = 末值 + 漂移 × τ。离散度 = K·√(A*/(1+θ²))，其中 A* = −2θ + (1 + 2(m−1)θ/m + θ²)(τ + τ²/m)，θ = 0.63，采用自由度为 m−1 的 Student-t 分位数。
5. **概率。** 直接由预测分布得到 P（第 Y 年的数值至少达到目标）。超出物理极限的目标概率为 0。
6. **长期加宽。** 超过 5 年后，物理类技术的范围最多加宽 40%（到第 10 年），因为物理类技术的长期预测比信息技术更容易出错。

</details>

<details>
<summary><b>自动修复</b></summary>

<br>

| 问题 | 检验 | 修复 |
|---|---|---|
| 产品混杂 | 同一年内的数值相差超过 3 倍 | 截至当时可得的最佳值（前沿） |
| 异常值 | 某一年的变化偏离典型值超过 5.5 个稳健标准差 | 稳健趋势（Theil–Sen）和稳健波动率（MAD） |
| 趋势改变 | 最近 15/10/8 年的漂移与之前相比，在 Farmer–Lafond 误差下 z > 3.2 | 只用最近的窗口拟合 |
| 物理极限 | 直线趋势在时间跨度内越过有来源的下限或上限 | 对距离极限的剩余差距建模，使进展在接近极限时放缓 |

修复由明确的检验决定，而不是尝试大量拟合再挑最好的。早期版本用的是后一种做法：它在真实数据上看起来更好，在干净的模拟数据上却更差，因为它在拟合噪声。

</details>

<details>
<summary><b>经验假设（每份报告中都会标出）</b></summary>

<br>

| 假设 | 数值 | 为什么属于经验判断 |
|---|---|---|
| 事件概率（到期日 / 3 年内） | 专利已授权 0.90/0.97 · 法规已颁布 0.75/0.92，已提议 0.30/0.55 · 产能已宣布 0.25/0.45，已做最终投资决定 0.60/0.85，在建 0.75/0.92 | 实测基准率很少；产能数值参考了氢能和电池项目的实际情况 |
| 成熟度 | 每个 TRL 步骤的年数中位数：软件 0.6、电子 1.3、硬件 2.0、能源 2.5、基础设施 3.0 | 关于 TRL 跨越时间的证据很少（GPS 从 TRL 3 到 9 用了 11.7 年） |
| 加宽 | 物理类领域：超过 5 年后离散度 × (1 + 0.4·(h−5)/5) | 方向有文献支持，幅度没有 |

</details>

<details>
<summary><b>单独运行引擎</b></summary>

<br>

```bash
cd skills/trend-predictor/scripts
python3 trend_predictor.py cpi                                   # 从 FRED 获取美国 CPI 年均值
python3 trend_predictor.py hindcast --end 2025                   # points.csv -> hindcast.csv, calibration.csv
python3 trend_predictor.py forecast --end 2025 --plots           # -> series_fit.csv, forecasts.csv, plots/
python3 trend_predictor.py feasibility --end 2025 --lead-years 2 --plots   # requirements.csv -> 项目评分
python3 trend_predictor.py workbook --project "…" --end 2025 --date 2026-10-16
```

CSV 结构见 [`SKILL.md`，Appendix B](../skills/trend-predictor/SKILL.md#appendix-b-csv-schemas)。

</details>

## 数据来源

所有来源都是免费的。报告会注明付费数据库能在哪些方面补充更多信息。

| 需求 | 使用的来源（免费） | 专业人士会补充的（付费） |
|---|---|---|
| 成本和性能历史 | Our World in Data、Santa Fe Performance Curve Database、Epoch AI、BLS / FRED、USGS、NREL、IEA、NHGRI、学习曲线论文、价目表 + Wayback Machine | BloombergNEF、拆解分析机构 |
| 带日期的事件 | 官方公报（Federal Register、EUR-Lex、各国公报）、Google Patents、Lens.org、ISO / IEC / IEEE | 法律和专利跟踪服务 |
| 判断输入 | Metaculus、Manifold、Good Judgment Open、公开的专家征询 | 委托的专家小组 |

## 局限

- **最多 10 年。** 范围在约 10–11 年内经过验证。超出之后，输出的是情景。
- **不预测采用速度。** 技能评估的是项目是否变得*可行*，而不是人们会多快购买它。没有任何方法能可靠地预测采用时间；唯一的测量是真实客户。
- **需要数据。** 年度变化少于 5 个的序列不会得到预测，嘈杂的序列会被报告为没有信息量。大多数领域只有少数几条又长又好的序列。
- **无法预见冲击。** 疫情、战争或突然的政策变化会让数值跑出范围。范围覆盖的是典型的意外，而不是所有意外。
- **部分数字是经验判断。** 事件、成熟度和加宽的假设都已标出，可以调整。
- **状态：v0.2，实验性。** 已在模拟数据、一次真实回测和一次（免费模型的）完整真实运行上测试，后者附评审一并发布。

## 常见问题

**它会动我的文件或账户吗？**
不会。它只读取公开网站，并且只写入自己的工作文件夹。

**为什么不直接问模型某件事何时可行？**
因为它会很有把握地给你一个日期，而你无法知道依据是什么。这个技能要求每个数字都有来源，在代码中完成计算，在每条序列自己的历史上检验方法，并把每个判断写成日后可以核对的形式。

**它和 PARADIGMA 有什么不同？**
PARADIGMA 描绘一个领域里已经发生的变化，以及谁在利用这些变化。TREND-PREDICTOR 为单个项目在未来日期的成功机会打分。先运行 PARADIGMA 找到该看哪里，再对你想在那里做的东西运行 TREND-PREDICTOR。

**10 年的概率可信吗？**
作为排序和合理性检查，可以。作为精确数字，不行：把 61% 理解为"如果趋势保持，可能性大于一半"，并关注报告给出的信号。

## 仓库结构

```text
trend-predictor-skill/
├── .claude-plugin/              Claude Code 插件市场与插件清单
├── skills/trend-predictor/
│   ├── SKILL.md                 智能体遵循的指令
│   └── scripts/trend_predictor.py   引擎（cpi、hindcast、forecast、feasibility、workbook）
├── tests/                       四个离线测试套件 + run_all.sh
│   └── results/                 最近一次运行的已提交输出（SUMMARY.md）
├── examples/                    真实数据回测 + 一次经过评审的免费模型真实运行
├── docs/research.md             方法背后的研究及其来源
├── dist/trend-predictor.zip     可直接上传到 Claude 应用的技能包（tools/package.sh）
├── tools/                       make_assets.py（README 插图）、package.sh（重建 ZIP）
├── README/                      本页的翻译
└── assets/                      横幅、流程图和可行性图
```

```bash
./tests/run_all.sh   # 运行所有套件并重写 tests/results/
```

## 参与贡献

欢迎提交 issue 和 pull request，尤其是：

- 你愿意分享到 `examples/` 的真实运行，最好附带日后可以核对的结果
- 某项技术的长期、干净、免费的数据序列
- 经验假设的更好基准率（事件延迟、TRL 跨越时间）

请保持规则不变：每个数字都要有来源，所有计算都留在引擎中。

## 许可证

[MIT](../LICENSE) © 2026 qaemu

<div align="center">
<br>
<sub>由 <a href="https://github.com/qaemu">qaemu</a> 构建。同一作者的其他作品：<a href="https://github.com/qaemu/paradigma-skill">PARADIGMA</a>，本技能所依托的约束变化全景工具；以及 <a href="https://github.com/qaemu/phasentic">Phasentic</a>，开源的粉末 X 射线衍射物相鉴定工具。</sub>
</div>
