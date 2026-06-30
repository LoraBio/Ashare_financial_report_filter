from typing import Protocol

from ..domain.models import AnalysisReport


class ReportNarrator(Protocol):
    def render(self, report: AnalysisReport) -> str: ...

