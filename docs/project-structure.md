---
title: 唐朝财报分析项目结构
aliases:
  - 项目结构
tags:
  - 唐朝财报分析
  - Python
  - 项目架构
  - 财报
---

# 唐朝财报分析项目结构

> [!summary] 项目目标
> 将财报取数、数据模型、指标计算、分析规则和文字输出拆开，使唐朝财报分析逻辑不依赖 AKShare 或具体大模型。

## 数据流

```mermaid
%%{init: {"themeVariables": {"fontSize": "12px"}} }%%  
flowchart LR
    A["AKShare / JSON / 年报"] --> B["parsers 与 providers：取数和转换"]
    B --> C["domain：统一财报模型"]
    C --> D["metrics：计算财务指标"]
    D --> E["analysis：执行单年及趋势规则"]
    E --> F["providers：生成文字报告"]
    F --> G["tools / cli：提供调用入口"]
```

核心原则：外部数据先转换为统一的 `FinancialSnapshot`，之后才进入指标和分析流程。更换数据源时，不应修改领域模型和分析规则。

## 目录树

```text
git_test/
├── README.md
├── pyproject.toml
├── config.example.toml
├── docs/
│   ├── book-outline.md
│   └── project-structure.md
├── examples/
│   └── sample_company.json
├── src/
│   └── tang_financial_analysis/
│       ├── __init__.py
│       ├── cli.py
│       ├── domain/
│       │   ├── __init__.py
│       │   └── models.py
│       ├── parsers/
│       │   ├── __init__.py
│       │   └── json_parser.py
│       ├── metrics/
│       │   ├── __init__.py
│       │   └── ratios.py
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── pipeline.py
│       │   └── trend.py
│       ├── ports/
│       │   ├── __init__.py
│       │   ├── financial_data.py
│       │   └── narrator.py
│       ├── providers/
│       │   ├── __init__.py
│       │   ├── akshare_data.py
│       │   └── plain_text.py
│       └── tools/
│           ├── __init__.py
│           └── analyze_company.py
└── tests/
    ├── __init__.py
    ├── test_akshare_provider.py
    ├── test_analysis.py
    ├── test_metrics.py
    └── test_trend.py
```

## 根目录文件

| 文件 | 用途 |
|---|---|
| `README.md` | 项目入口，说明目标、架构、安装方式和常用命令。 |
| `pyproject.toml` | Python 项目配置；定义包名、Python 版本、依赖、命令行入口和测试配置。 |
| `config.example.toml` | 配置示例；用于记录分析阈值和输出供应商，但不存放密钥。 |
| `《手把手教你读财报》唐朝.pdf` | 项目的知识来源。它是扫描版原书，不属于程序代码。 |
| `fruits.txt` | 与当前项目无关的原有文件，可以保留或以后清理。 |

## 文档与示例

### `docs/`

| 文件 | 用途 |
|---|---|
| `book-outline.md` | 根据原书目录建立的实现索引，记录已覆盖规则和待读书验证内容。 |
| `project-structure.md` | 本文档，供 Obsidian 查看项目结构与职责边界。 |

### `examples/`

| 文件 | 用途 |
|---|---|
| `sample_company.json` | 标准财报快照示例，可在无网络环境下演示单年分析。 |

## 核心源码

所有 Python 源码位于 `src/tang_financial_analysis/`。采用 `src` 布局可以避免测试意外导入仓库根目录中的同名代码。

### `domain/`：领域模型

| 文件 | 用途 |
|---|---|
| `models.py` | 定义 `FinancialSnapshot`、`AnalysisReport`、`TrendReport`、风险信号和严重程度。它是各模块共同使用的稳定语言。 |
| `__init__.py` | 对外集中导出领域模型。 |

这里不应出现 AKShare、HTTP、命令行或大模型代码。

### `parsers/`：文件解析

| 文件 | 用途 |
|---|---|
| `json_parser.py` | 将标准 JSON 文件转换为 `FinancialSnapshot`，并使用 `Decimal` 保存金额。 |
| `__init__.py` | 导出 JSON 解析入口。 |

未来 PDF、Excel、XBRL 解析器应放在这里。解析器只负责识别和标准化数据，不负责判断企业好坏。

### `metrics/`：指标计算

| 文件 | 用途 |
|---|---|
| `ratios.py` | 计算货币资金/有息负债、应收/收入、资产负债率、毛利率、净利率、ROE 和现金利润比。 |
| `__init__.py` | 导出指标计算函数。 |

指标函数应尽量保持为纯函数：相同输入永远得到相同输出，不读取网络和配置。

### `analysis/`：分析规则

| 文件 | 用途 |
|---|---|
| `pipeline.py` | 单年度分析流程；执行债务、应收账款及经营现金流初筛，并生成结构化信号。 |
| `trend.py` | 至少五个完整年度的趋势分析；计算复合增长率、五年累计值和持续性风险。 |
| `__init__.py` | 导出单年及趋势分析入口。 |

唐朝逻辑的主要实现位置是这里。新增规则时，需要同时写清适用条件、阈值依据和测试。

### `ports/`：抽象接口

| 文件 | 用途 |
|---|---|
| `financial_data.py` | 定义财务数据提供者协议，约束单年和多年数据获取能力。 |
| `narrator.py` | 定义报告表达协议，使分析结果不依赖具体大模型。 |
| `__init__.py` | 统一导出协议。 |

`ports` 只描述系统需要什么，不负责具体实现。这是“领域逻辑与供应商解耦”的关键。

### `providers/`：外部能力实现

| 文件 | 用途 |
|---|---|
| `akshare_data.py` | 调用 AKShare 获取三大表，选择三表均完整的年度，并映射成统一财报模型。 |
| `plain_text.py` | 将结构化的单年和五年分析报告转换为确定性文本。 |
| `__init__.py` | 导出当前提供者实现。 |

以后接入其他数据源或大模型时，应新增 provider，而不是把供应商代码写进 `analysis/`。

### `tools/`：Agent 工具接口

| 文件 | 用途 |
|---|---|
| `analyze_company.py` | 为 Agent 和 CLI 提供稳定的高层函数：分析 JSON、单年股票和多年趋势。 |
| `__init__.py` | 导出工具函数。 |

这里负责组合已有模块，不放置新的财务判断规则。

### `cli.py`：命令行入口

提供三种操作：

```powershell
# 分析本地 JSON
python -m tang_financial_analysis.cli analyze examples/sample_company.json

# 分析指定年度
python -m tang_financial_analysis.cli stock 002893 --year 2025

# 分析最近五个完整年报年度
python -m tang_financial_analysis.cli trend 002893 --years 5
```

## 测试结构

| 文件 | 验证内容 |
|---|---|
| `test_metrics.py` | 除零处理和核心指标计算。 |
| `test_analysis.py` | 单年债务、应收和现金转化风险信号。 |
| `test_akshare_provider.py` | 股票代码规范化以及三大表字段映射；测试过程不依赖网络。 |
| `test_trend.py` | 五年数据要求、年度排序和趋势指标。 |

运行全部测试：

```powershell
python -m pytest -q
```

## 阅读代码的推荐顺序

1. `domain/models.py`：先理解系统使用的数据语言。
2. `metrics/ratios.py`：理解原始科目如何变成指标。
3. `analysis/pipeline.py`：理解单年风险判断。
4. `analysis/trend.py`：理解五年趋势如何减少单年误判。
5. `providers/akshare_data.py`：理解外部数据如何适配领域模型。
6. `tools/analyze_company.py`：理解各层如何组合。
7. `cli.py`：理解用户命令如何进入系统。

## 新功能应该放在哪里

| 新需求 | 位置 |
|---|---|
| 增加财务字段 | `domain/models.py`，随后更新解析与测试 |
| 增加财务比率 | `metrics/` |
| 增加唐朝分析规则 | `analysis/` |
| 接入新财务数据源 | `providers/`，实现 `ports/financial_data.py` 协议 |
| 读取新文件格式 | `parsers/` |
| 接入 OpenAI 或其他模型 | `providers/`，实现 `ports/narrator.py` 协议 |
| 增加 Agent 可调用动作 | `tools/` |
| 增加命令 | `cli.py` |

## Obsidian 使用建议

可以将整个仓库作为 Obsidian Vault 打开，或只把 `docs/` 加入现有 Vault。建议后续为每条分析规则建立独立笔记，并通过双向链接关联：

```text
[[book-outline]]
[[project-structure]]
[[应收账款分析规则]]
[[经营现金流与净利润]]
```

> [!warning] 当前边界
> 目前模型只覆盖有限财务字段与初筛规则，还没有财报附注、审计意见、补贴明细、季度季节性和同行比较。输出属于研究辅助，不构成投资建议。
