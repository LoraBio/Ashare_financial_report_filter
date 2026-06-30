from decimal import Decimal
from math import isnan
from typing import Any, Mapping

from ..domain.models import FinancialSnapshot


def sina_code(stock_code: str) -> str:
    code = stock_code.strip().lower()
    if code.startswith(("sz", "sh", "bj")):
        return code
    if len(code) != 6 or not code.isdigit():
        raise ValueError("股票代码应为 6 位数字，例如 002893")
    prefix = "sh" if code.startswith(("5", "6", "9")) else "bj" if code.startswith(("4", "8")) else "sz"
    return prefix + code


def _money(row: Mapping[str, Any], name: str) -> Decimal:
    value = row.get(name, 0)
    if value is None or (isinstance(value, float) and isnan(value)):
        return Decimal("0")
    return Decimal(str(value))


def snapshot_from_rows(
    stock_code: str,
    balance: Mapping[str, Any],
    income: Mapping[str, Any],
    cashflow: Mapping[str, Any],
) -> FinancialSnapshot:
    revenue = _money(income, "营业收入") or _money(income, "营业总收入")
    cost = _money(income, "营业成本")
    debt_fields = ("短期借款", "一年内到期的非流动负债", "长期借款", "应付债券", "租赁负债")
    return FinancialSnapshot(
        company=f"京能热力（{stock_code}）" if stock_code == "002893" else stock_code,
        period=str(balance["报告日"]),
        currency=str(balance.get("币种", "CNY")),
        cash=_money(balance, "货币资金"),
        interest_bearing_debt=sum((_money(balance, field) for field in debt_fields), Decimal("0")),
        accounts_receivable=_money(balance, "应收账款"),
        total_assets=_money(balance, "资产总计"),
        total_liabilities=_money(balance, "负债合计"),
        equity=_money(balance, "所有者权益(或股东权益)合计"),
        revenue=revenue,
        gross_profit=revenue - cost,
        net_profit=_money(income, "净利润"),
        operating_cash_flow=_money(cashflow, "经营活动产生的现金流量净额"),
    )


class AkShareFinancialDataProvider:
    """AKShare 只负责取数和字段映射，不包含分析规则。"""

    @staticmethod
    def _frames(stock_code: str):
        try:
            import akshare as ak
        except ImportError as exc:
            raise RuntimeError('请先安装数据依赖：python -m pip install -e ".[data]"') from exc

        code = sina_code(stock_code)
        return {
            name: ak.stock_financial_report_sina(stock=code, symbol=name)
            for name in ("资产负债表", "利润表", "现金流量表")
        }

    def annual_snapshot(self, stock_code: str, year: int | None = None) -> FinancialSnapshot:
        frames = self._frames(stock_code)
        report_date = f"{year}1231" if year else None
        rows = []
        for name, frame in frames.items():
            annual = frame[frame["报告日"].astype(str).str.endswith("1231")]
            if report_date:
                annual = annual[annual["报告日"].astype(str) == report_date]
            if annual.empty:
                raise ValueError(f"{stock_code} 没有找到目标年度{name}")
            rows.append(annual.iloc[0])
        return snapshot_from_rows(stock_code, *rows)

    def annual_snapshots(self, stock_code: str, years: int = 5) -> tuple[FinancialSnapshot, ...]:
        if years < 1:
            raise ValueError("年度数量至少为 1")
        frames = self._frames(stock_code)
        annual_dates: dict[str, set[str]] = {}
        for name, frame in frames.items():
            dates = frame["报告日"].astype(str)
            annual_dates[name] = set(dates[dates.str.endswith("1231")])
        common_dates = sorted(set.intersection(*annual_dates.values()), reverse=True)
        selected = sorted(common_dates[:years])
        snapshots = []
        for report_date in selected:
            rows = []
            for frame in frames.values():
                rows.append(frame[frame["报告日"].astype(str) == report_date].iloc[0])
            snapshots.append(snapshot_from_rows(stock_code, *rows))
        return tuple(snapshots)

    def latest_periodic_snapshot(self, stock_code: str) -> FinancialSnapshot | None:
        frames = self._frames(stock_code)
        common = sorted(set.intersection(*(set(f["报告日"].astype(str)) for f in frames.values())), reverse=True)
        periodic = [date for date in common if not date.endswith("1231")]
        if not periodic:
            return None
        report_date = periodic[0]
        rows = [frame[frame["报告日"].astype(str) == report_date].iloc[0] for frame in frames.values()]
        return snapshot_from_rows(stock_code, *rows)

    @staticmethod
    def disclosure_fallback(stock_code: str) -> tuple[str, ...]:
        import akshare as ak
        from datetime import date
        frame = ak.stock_zh_a_disclosure_report_cninfo(
            symbol=stock_code, market="沪深京", category="首发",
            start_date="19900101", end_date=date.today().strftime("%Y%m%d"),
        )
        if frame.empty:
            return ()
        matched = frame[frame["公告标题"].astype(str).str.contains("招股|上市公告", regex=True)]
        return tuple(f"{row['公告标题']}｜{row['公告链接']}" for _, row in matched.iterrows())
