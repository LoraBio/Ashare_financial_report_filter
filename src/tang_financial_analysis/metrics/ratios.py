from decimal import Decimal

from ..domain.models import FinancialSnapshot


def safe_div(numerator: Decimal, denominator: Decimal) -> Decimal | None:
    return None if denominator == 0 else numerator / denominator


def calculate(snapshot: FinancialSnapshot) -> dict[str, Decimal | None]:
    return {
        "cash_to_debt": safe_div(snapshot.cash, snapshot.interest_bearing_debt),
        "receivables_to_revenue": safe_div(snapshot.accounts_receivable, snapshot.revenue),
        "debt_ratio": safe_div(snapshot.total_liabilities, snapshot.total_assets),
        "gross_margin": safe_div(snapshot.gross_profit, snapshot.revenue),
        "net_margin": safe_div(snapshot.net_profit, snapshot.revenue),
        "roe": safe_div(snapshot.net_profit, snapshot.equity),
        "cash_profit_ratio": safe_div(snapshot.operating_cash_flow, snapshot.net_profit),
    }

