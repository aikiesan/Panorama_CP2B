"""
Models Module - Data Structures for Biogas Research
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)
"""

from .residue_models import (
    ParameterRange,
    ChemicalParameters,
    AvailabilityFactors,
    OperationalParameters,
    ScientificReference,
    ResidueData
)

__all__ = [
    'ParameterRange',
    'ChemicalParameters',
    'AvailabilityFactors',
    'OperationalParameters',
    'ScientificReference',
    'ResidueData'
]
