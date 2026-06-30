import argparse

from .tools.analyze_company import analyze_financial_file, analyze_stock, analyze_stock_trend


def main() -> None:
    parser = argparse.ArgumentParser(prog="tang-report", description="唐朝财报分析工具")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze_cmd = sub.add_parser("analyze", help="分析标准 JSON 财报快照")
    analyze_cmd.add_argument("file")
    stock_cmd = sub.add_parser("stock", help="通过 AKShare 获取并分析 A 股年报")
    stock_cmd.add_argument("code", help="6 位股票代码")
    stock_cmd.add_argument("--year", type=int, help="报告年度；默认最新年报")
    trend_cmd = sub.add_parser("trend", help="通过 AKShare 分析最近完整年报趋势")
    trend_cmd.add_argument("code", help="6 位股票代码")
    trend_cmd.add_argument("--years", type=int, default=5, help="年度数量，默认 5")
    args = parser.parse_args()
    if args.command == "analyze":
        print(analyze_financial_file(args.file))
    elif args.command == "stock":
        print(analyze_stock(args.code, args.year))
    elif args.command == "trend":
        print(analyze_stock_trend(args.code, args.years))


if __name__ == "__main__":
    main()
