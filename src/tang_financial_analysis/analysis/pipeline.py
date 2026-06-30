from decimal import Decimal

from ..domain.models import AnalysisReport, FinancialSnapshot, Severity, Signal
from ..metrics.ratios import calculate


def analyze(snapshot: FinancialSnapshot) -> AnalysisReport:
    """先排除明显风险，再描述质量；阈值是待读书校准的显式假设。"""
    metrics = calculate(snapshot)
    signals: list[Signal] = []

    if snapshot.interest_bearing_debt > snapshot.cash:
        signals.append(Signal("DEBT_CASH_GAP", Severity.WARNING, "有息负债高于货币资金", "偿债安全边际需要结合受限资金和债务期限继续核实。"))
    if (r := metrics["receivables_to_revenue"]) is not None and r > Decimal("0.30"):
        signals.append(Signal("HIGH_RECEIVABLES", Severity.WARNING, "应收账款占收入偏高", "收入的现金含量可能较弱，应核对账龄、坏账准备和主要客户。", {"ratio": f"{r:.2%}"}))
    if snapshot.net_profit > 0 and (r := metrics["cash_profit_ratio"]) is not None and r < Decimal("0.80"):
        signals.append(Signal("WEAK_CASH_CONVERSION", Severity.DANGER, "经营现金流弱于净利润", "利润尚未充分转化为现金，应检查应收、存货和收入确认。", {"ratio": f"{r:.2f}"}))
    if not signals:
        signals.append(Signal("NO_INITIAL_RED_FLAG", Severity.INFO, "未发现初筛红旗", "仅代表当前有限字段通过初筛，不代表企业没有风险。"))

    return AnalysisReport(snapshot.company, snapshot.period, metrics, tuple(signals))

