"""
Services Layer - Business Logic
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Centralize business logic separate from UI
This layer contains pure calculation and analysis logic, following SOLID principles.
"""

from .availability_calculator import AvailabilityCalculator
from .scenario_manager import ScenarioManager
from .contribution_analyzer import ContributionAnalyzer

__all__ = [
    'AvailabilityCalculator',
    'ScenarioManager',
    'ContributionAnalyzer'
]
