from dataclasses import replace
from decimal import Decimal

from tang_financial_analysis.analysis.trend import analyze_trend
from tests.test_metrics import sample


def history(count: int = 5):
    base = sample()
    return tuple(
        replace(
            base,
            period=f"{2021 + i}1231",
            revenue=Decimal(400 + i * 25),
            accounts_receivable=Decimal(140 + i * 10),
        )
        for i in range(count)
    )


def test_uses_three_years_with_reduced_confidence() -> None:
    result = analyze_trend(history(3))
    assert len(result.snapshots) == 3
    assert "LIMITED_HISTORY" in {signal.code for signal in result.signals}


def test_uses_one_year_without_growth_rate() -> None:
    result = analyze_trend(history(1))
    assert result.trend_metrics["revenue_cagr"] is None


def test_analyzes_five_years_in_order() -> None:
    result = analyze_trend(tuple(reversed(history())))
    assert result.snapshots[0].period == "20211231"
    assert result.snapshots[-1].period == "20251231"
    assert result.trend_metrics["revenue_cagr"] is not None
