已搭好“唐朝财报分析”Python 项目骨架。

包含：

- 财报领域模型与 JSON 解析
- 7 个基础财务指标
- 债务、应收款、现金流三类初筛规则
- 分析逻辑与模型供应商解耦
- Agent 工具接口与命令行入口
- 示例数据、配置示例和基础测试
- 按原书目录建立的实现索引

主要入口：

- [README.md](C:/Users/57045/git_test/README.md)
- [项目结构](C:/Users/57045/git_test/src/tang_financial_analysis)
- [原书实现索引](C:/Users/57045/git_test/docs/book-outline.md)
- [示例财报](C:/Users/57045/git_test/examples/sample_company.json)

第一步：定义统一的“财报数据模型”。

原因是后续无论数据来自年报 PDF、Excel、接口还是手工录入，都必须转换成同一种结构，分析规则才不会与数据来源绑定。

当前已有初版 `FinancialSnapshot`，下一步应将它扩展为：

- 资产负债表
- 利润表
- 现金流量表
- 公司与报告期信息
- 原始数据来源和页码
- 多年度数据结构

建议先用一家真实公司最近 5 年年报作为样本，逐项完善数据模型和测试。

