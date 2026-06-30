from decimal import Decimal

from ..domain.models import FinancialSnapshot, Severity, Signal, TrendReport
from .pipeline import analyze


def _growth(first: Decimal, last: Decimal, periods: int) -> Decimal | None:
    if first <= 0 or last < 0 or periods <= 0:
        return None
    return Decimal(str((float(last / first) ** (1 / periods)) - 1))


def analyze_trend(snapshots: tuple[FinancialSnapshot, ...]) -> TrendReport:
    if not snapshots:
        raise ValueError("趋势分析至少需要一个完整年度")
    ordered = tuple(sorted(snapshots, key=lambda item: item.period))
    reports = tuple(analyze(item) for item in ordered)
    first, last = ordered[0], ordered[-1]
    periods = len(ordered) - 1
    metrics = {
        "revenue_cagr": _growth(first.revenue, last.revenue, periods),
        "net_profit_cagr": _growth(first.net_profit, last.net_profit, periods),
        "operating_cash_flow_period_sum": sum((x.operating_cash_flow for x in ordered), Decimal("0")),
        "net_profit_period_sum": sum((x.net_profit for x in ordered), Decimal("0")),
    }
    signals: list[Signal] = []
    if len(ordered) < 5:
        signals.append(Signal("LIMITED_HISTORY", Severity.WARNING, "历史年报不足五年", f"目前只有 {len(ordered)} 个三表齐全年度，已按现有数据分析；趋势结论可信度较低。"))
    high_receivable_years = sum(
        1 for report in reports
        if (report.metrics["receivables_to_revenue"] or Decimal("0")) > Decimal("0.30")
    )
    weak_cash_years = sum(
        1 for item in ordered
        if item.net_profit > 0 and item.operating_cash_flow / item.net_profit < Decimal("0.80")
    )
    persistent_threshold = 3 if len(ordered) >= 5 else max(2, len(ordered))
    if high_receivable_years >= persistent_threshold:
        signals.append(Signal("PERSISTENT_HIGH_RECEIVABLES", Severity.WARNING, "应收账款长期偏高", f"{len(ordered)} 年中有 {high_receivable_years} 年应收账款超过营业收入的 30%。"))
    if weak_cash_years >= persistent_threshold:
        signals.append(Signal("PERSISTENT_WEAK_CASH", Severity.DANGER, "利润现金转化长期偏弱", f"{len(ordered)} 年中有 {weak_cash_years} 年经营现金流不足净利润的 80%。"))
    if not signals:
        signals.append(Signal("NO_PERSISTENT_TREND_RED_FLAG", Severity.INFO, "未发现持续性趋势红旗", "季节性和确认时点仍需结合季度及附注判断。"))
    mode = "单点分析（不计算增长率）" if len(ordered) == 1 else f"{len(ordered)} 年趋势分析"
    return TrendReport(
        ordered, reports, metrics, tuple(signals),
        reports_used=tuple(f"{item.period[:4]} 年年度报告（三大表）" for item in ordered),
        data_source="AKShare / 新浪财经财务报表接口",
        analysis_mode=mode,
        limitations=("年度数据不能识别季内波动。", "补贴确认、应收账款账龄和受限资金仍需查阅附注。", "历史变化不能直接推断未来表现。"),
    )
