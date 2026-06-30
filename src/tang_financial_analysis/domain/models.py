from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"


@dataclass(frozen=True)
class FinancialSnapshot:
    company: str
    period: str
    currency: str
    cash: Decimal
    interest_bearing_debt: Decimal
    accounts_receivable: Decimal
    total_assets: Decimal
    total_liabilities: Decimal
    equity: Decimal
    revenue: Decimal
    gross_profit: Decimal
    net_profit: Decimal
    operating_cash_flow: Decimal


@dataclass(frozen=True)
class Signal:
    code: str
    severity: Severity
    title: str
    detail: str
    evidence: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class AnalysisReport:
    company: str
    period: str
    metrics: dict[str, Decimal | None]
    signals: tuple[Signal, ...]


@dataclass(frozen=True)
class TrendReport:
    snapshots: tuple[FinancialSnapshot, ...]
    annual_reports: tuple[AnalysisReport, ...]
    trend_metrics: dict[str, Decimal | None]
    signals: tuple[Signal, ...]
    reports_used: tuple[str, ...] = ()
    data_source: str = ""
    analysis_mode: str = ""
    limitations: tuple[str, ...] = ()
