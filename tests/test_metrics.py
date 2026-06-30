from decimal import Decimal

from tang_financial_analysis.domain.models import FinancialSnapshot
from tang_financial_analysis.metrics.ratios import calculate, safe_div


def sample() -> FinancialSnapshot:
    return FinancialSnapshot("公司", "2025", "CNY", *(Decimal(x) for x in [120, 200, 180, 1000, 600, 400, 500, 180, 50, 25]))


def test_safe_div_handles_zero() -> None:
    assert safe_div(Decimal("1"), Decimal("0")) is None


def test_calculates_core_ratios() -> None:
    metrics = calculate(sample())
    assert metrics["gross_margin"] == Decimal("0.36")
    assert metrics["cash_profit_ratio"] == Decimal("0.5")

