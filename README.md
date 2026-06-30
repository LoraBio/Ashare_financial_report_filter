# 唐朝财报分析 Agent

Stock selection based on companies' financial reports.

这是一个边读《手把手教你读财报》、边实现分析规则的学习型 Python 项目。当前版本先建立稳定边界：财报数据、指标计算和分析规则不依赖任何大模型；模型只负责把结构化结论组织成自然语言。

## 架构

```text
原始财报 -> parser(解析) -> domain(标准数据)
                              |
                              v
                         metrics(指标)
                              |
                              v
                         analysis(规则)
                              |
                              v
                    ports -> providers(表达层)
```

- `domain`：财务数据、结论和风险信号的数据模型。
- `parsers`：未来接入 PDF、Excel、交易所 XBRL；目前提供 JSON 解析器。
- `metrics`：纯函数计算，便于单元测试。
- `analysis`：按“先排雷，再理解盈利质量，最后谈估值”的流程编排。
- `ports`：模型供应商抽象接口。
- `providers`：确定性文本输出；以后可新增 OpenAI 等实现而不改领域层。
- `tools`：供 Agent 调用的稳定工具函数。
- `cli`：本地命令行入口。

## 快速开始

```powershell
python -m pip install -e ".[dev]"
tang-report analyze examples/sample_company.json
pytest
```

分析真实 A 股（AKShare 为可替换的数据提供层）：

```powershell
python -m pip install -e ".[data,dev]"
tang-report stock 002893 --year 2025
tang-report trend 002893 --years 5
```

请求五年但数据不足时，工具自动使用全部可用完整年度并标注可信度；只有一年时退化为单年分析，没有完整年报时给出季度报告或招股书的后续建议。

也可不安装直接运行：

```powershell
$env:PYTHONPATH="src"
python -m tang_financial_analysis.cli analyze examples/sample_company.json
```

## 学习路线

1. 先在 `docs/book-outline.md` 记录每章观点，并把可验证观点改写成规则。
2. 给规则补“正常、边界、异常”三个测试，再写实现。
3. 接入真实年报解析器；解析结果必须统一为 `FinancialSnapshot`。
4. 累积多年度数据，加入趋势、同行对比和财报附注证据。
5. 最后才接模型供应商；模型不得自行发明财务数字或规则结论。

> 当前代码是教学骨架，不构成投资建议。阈值只是可配置的初始假设，需要随阅读逐条校正并注明出处。
