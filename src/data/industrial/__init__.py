"""
Industrial Sector Registry
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Register all industrial residues
Phase 3 Complete: 4 residues implemented (Laticínios x2, Cervejarias, Frigoríficos)
"""

# Import all industrial residues
from src.data.industrial.soro_de_laticinios_leite import SORO_LATICINIOS_LEITE_DATA
from src.data.industrial.soro_de_laticinios_derivados import SORO_LATICINIOS_DERIVADOS_DATA
from src.data.industrial.bagaco_cervejarias import BAGACO_CERVEJARIAS_DATA
from src.data.industrial.efluente_frigorificos import EFLUENTE_FRIGORIFICOS_DATA
from src.data.industrial.soro_de_queijo import SORO_DE_QUEIJO_DATA

# Registry of all industrial residues
INDUSTRIAL_RESIDUES = {
    "Soro de Laticínios (Leite)": SORO_LATICINIOS_LEITE_DATA,
    "Soro de Laticínios (Derivados)": SORO_LATICINIOS_DERIVADOS_DATA,
    "Bagaço de Cervejarias": BAGACO_CERVEJARIAS_DATA,
    "Efluente de Frigoríficos": EFLUENTE_FRIGORIFICOS_DATA,
    "Soro de queijo": SORO_DE_QUEIJO_DATA,
}

# Sector metadata
INDUSTRIAL_SECTOR_INFO = {
    "name": "Industrial",
    "icon": "🏭",
    "description": "Efluentes e resíduos industriais",
    "color": "#8b5cf6",
    "gradient": "linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%)",
    "border_color": "#8b5cf6",
    "residues": list(INDUSTRIAL_RESIDUES.keys())
}

__all__ = [
    'INDUSTRIAL_RESIDUES',
    'INDUSTRIAL_SECTOR_INFO',
    'SORO_LATICINIOS_LEITE_DATA',
    'SORO_LATICINIOS_DERIVADOS_DATA',
    'BAGACO_CERVEJARIAS_DATA',
    'EFLUENTE_FRIGORIFICOS_DATA',
]
