from typing import Protocol

from ..domain.models import FinancialSnapshot


class FinancialDataProvider(Protocol):
    def annual_snapshot(self, stock_code: str, year: int | None = None) -> FinancialSnapshot: ...

    def annual_snapshots(self, stock_code: str, years: int = 5) -> tuple[FinancialSnapshot, ...]: ...
