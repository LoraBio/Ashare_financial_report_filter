from ..analysis.pipeline import analyze
from ..analysis.trend import analyze_trend
from ..parsers.json_parser import parse_json
from ..providers.plain_text import PlainTextNarrator
from ..providers.akshare_data import AkShareFinancialDataProvider


def analyze_financial_file(path: str) -> str:
    """供 CLI 或未来 Agent 工具层复用的稳定入口。"""
    return PlainTextNarrator().render(analyze(parse_json(path)))


def analyze_stock(stock_code: str, year: int | None = None) -> str:
    snapshot = AkShareFinancialDataProvider().annual_snapshot(stock_code, year)
    return PlainTextNarrator().render(analyze(snapshot))


def analyze_stock_trend(stock_code: str, years: int = 5) -> str:
    provider = AkShareFinancialDataProvider()
    snapshots = provider.annual_snapshots(stock_code, years)
    narrator = PlainTextNarrator()
    if snapshots:
        return narrator.render_trend(analyze_trend(snapshots))
    periodic = provider.latest_periodic_snapshot(stock_code)
    if periodic is not None:
        return (
            "分析说明：\n"
            f"- 使用报告：{periodic.period} 中报/季报（三大表）\n"
            f"- 覆盖期间：{periodic.period}\n"
            "- 数据来源：AKShare / 新浪财经财务报表接口\n"
            "- 分析模式：非年度单点分析（不计算增长率）\n"
            "- 不可过度推断：累计数据不能简单年化；不能据此判断全年趋势，季节性行业尤其如此。\n\n"
            + narrator.render(analyze(periodic))
        )
    documents = provider.disclosure_fallback(stock_code)
    if documents:
        return (
            "分析说明：\n- 使用报告：" + "；".join(documents) +
            "\n- 覆盖期间：发行上市阶段\n- 数据来源：AKShare / 巨潮资讯公告接口"
            "\n- 分析模式：文档兜底（无结构化比率）"
            "\n- 不可过度推断：未取得可比三大表，不能计算增长率、趋势或财务质量指标。"
        )
    return (
        "分析说明：\n- 使用报告：无\n- 覆盖期间：无\n- 数据来源：AKShare"
        "\n- 分析模式：无可用数据\n- 不可过度推断：没有结构化报表或发行文件，不能形成财务结论。"
    )
