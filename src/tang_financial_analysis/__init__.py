"""唐朝财报分析的领域核心。"""

from .analysis.pipeline import analyze
from .domain.models import FinancialSnapshot

__all__ = ["FinancialSnapshot", "analyze"]

