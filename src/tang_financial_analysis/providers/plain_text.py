from decimal import Decimal

from ..domain.models import AnalysisReport, TrendReport


class PlainTextNarrator:
    def render(self, report: AnalysisReport) -> str:
        lines = [f"{report.company}（{report.period}）", "", "初筛结论："]
        lines.extend(f"- [{s.severity}] {s.title}：{s.detail}" for s in report.signals)
        lines.extend(["", "关键指标："])
        for name, value in report.metrics.items():
            lines.append(f"- {name}: {'N/A' if value is None else f'{value:.4f}'}")
        return "\n".join(lines)

    def render_trend(self, trend: TrendReport) -> str:
        latest_text = self.render(trend.annual_reports[-1])
        count = len(trend.snapshots)
        title = "五年趋势" if count >= 5 else f"现有 {count} 年分析（不足五年）"
        lines = [
            "分析说明：",
            f"- 使用报告：{'；'.join(trend.reports_used)}",
            f"- 覆盖期间：{trend.snapshots[0].period}-{trend.snapshots[-1].period}",
            f"- 数据来源：{trend.data_source}",
            f"- 分析模式：{trend.analysis_mode}",
            "- 不可过度推断：" + "；".join(trend.limitations),
            "", latest_text, "", f"{title}（{trend.snapshots[0].period[:4]}-{trend.snapshots[-1].period[:4]}）：",
        ]
        lines.append("年度 | 营业收入(亿元) | 净利润(亿元) | 经营现金流(亿元) | 应收/收入 | ROE")
        for snapshot, report in zip(trend.snapshots, trend.annual_reports, strict=True):
            ratio = report.metrics["receivables_to_revenue"]
            roe = report.metrics["roe"]
            lines.append(
                f"{snapshot.period[:4]} | {snapshot.revenue / Decimal('100000000'):.2f} | "
                f"{snapshot.net_profit / Decimal('100000000'):.2f} | "
                f"{snapshot.operating_cash_flow / Decimal('100000000'):.2f} | "
                f"{'N/A' if ratio is None else f'{ratio:.1%}'} | {'N/A' if roe is None else f'{roe:.1%}'}"
            )
        lines.extend(["", "趋势指标："])
        for name, value in trend.trend_metrics.items():
            lines.append(f"- {name}: {'N/A' if value is None else f'{value:.4f}'}")
        lines.extend(["", "趋势结论："])
        lines.extend(f"- [{s.severity}] {s.title}：{s.detail}" for s in trend.signals)
        return "\n".join(lines)
