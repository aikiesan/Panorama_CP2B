"""
Agricultura Sector Registry
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Register all agriculture residues
"""

from .cana_vinhaca import VINHACA_DE_CANA_DE_ACUCAR_DATA
from .cana_palha import PALHA_DE_CANA_DE_ACUCAR_PALHICO_DATA
from .cana_torta import TORTA_DE_FILTRO_FILTER_CAKE_DATA

# Registry of all agricultura residues
AGRICULTURA_RESIDUES = {
    "Vinhaça de Cana-de-açúcar": VINHACA_DE_CANA_DE_ACUCAR_DATA,
    "Palha de Cana-de-açúcar (Palhiço)": PALHA_DE_CANA_DE_ACUCAR_PALHICO_DATA,
    "Torta de Filtro (Filter Cake)": TORTA_DE_FILTRO_FILTER_CAKE_DATA,
}

# Sector metadata
AGRICULTURA_SECTOR_INFO = {
    "name": "Agricultura",
    "icon": "🌾",
    "description": "Resíduos agrícolas e agroindustriais",
    "color": "#059669",
    "gradient": "linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)",
    "border_color": "#059669",
    "residues": list(AGRICULTURA_RESIDUES.keys())
}

__all__ = [
    'AGRICULTURA_RESIDUES',
    'AGRICULTURA_SECTOR_INFO',
    'VINHACA_DE_CANA_DE_ACUCAR_DATA',
    'PALHA_DE_CANA_DE_ACUCAR_PALHICO_DATA',
    'TORTA_DE_FILTRO_FILTER_CAKE_DATA',
]
