from decimal import Decimal

from tang_financial_analysis.providers.akshare_data import sina_code, snapshot_from_rows


def test_normalizes_stock_code() -> None:
    assert sina_code("002893") == "sz002893"
    assert sina_code("600000") == "sh600000"


def test_maps_statement_rows_without_network() -> None:
    balance = {"报告日": "20251231", "币种": "CNY", "货币资金": 90, "短期借款": 20,
               "一年内到期的非流动负债": 10, "长期借款": 5, "租赁负债": 1,
               "应收账款": 46, "资产总计": 300, "负债合计": 160,
               "所有者权益(或股东权益)合计": 140}
    income = {"营业收入": 130, "营业成本": 100, "净利润": 8}
    cashflow = {"经营活动产生的现金流量净额": 14}
    result = snapshot_from_rows("002893", balance, income, cashflow)
    assert result.interest_bearing_debt == Decimal("36")
    assert result.gross_profit == Decimal("30")
