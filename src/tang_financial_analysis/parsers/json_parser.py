import json
from decimal import Decimal
from pathlib import Path

from ..domain.models import FinancialSnapshot


MONEY_FIELDS = {
    "cash", "interest_bearing_debt", "accounts_receivable", "total_assets",
    "total_liabilities", "equity", "revenue", "gross_profit", "net_profit",
    "operating_cash_flow",
}


def parse_json(path: str | Path) -> FinancialSnapshot:
    data = json.loads(Path(path).read_text(encoding="utf-8"), parse_float=Decimal)
    for key in MONEY_FIELDS:
        data[key] = Decimal(str(data[key]))
    return FinancialSnapshot(**data)

