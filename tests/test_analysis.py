from tang_financial_analysis.analysis.pipeline import analyze
from tests.test_metrics import sample


def test_flags_cash_conversion_and_debt() -> None:
    codes = {signal.code for signal in analyze(sample()).signals}
    assert {"DEBT_CASH_GAP", "HIGH_RECEIVABLES", "WEAK_CASH_CONVERSION"} <= codes

