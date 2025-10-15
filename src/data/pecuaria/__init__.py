"""
Pecuária Sector Registry
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Register all livestock residues
"""

from .avicultura_frango import DEJETO_DE_AVES_CAMA_DE_FRANGO_DATA
from .avicultura_codornas import DEJETO_DE_CODORNAS_DATA
from .bovinocultura import DEJETOS_DE_BOVINOS_LEITE__CORTE_DATA
from .suinocultura import DEJETOS_DE_SUINOS_DATA

# Registry of all pecuaria residues
PECUARIA_RESIDUES = {
    "Dejeto de Aves (Cama de Frango)": DEJETO_DE_AVES_CAMA_DE_FRANGO_DATA,
    "Dejeto de Codornas": DEJETO_DE_CODORNAS_DATA,
    "Dejetos de Bovinos (Leite + Corte)": DEJETOS_DE_BOVINOS_LEITE__CORTE_DATA,
    "Dejetos de Suínos": DEJETOS_DE_SUINOS_DATA,
}

# Sector metadata
PECUARIA_SECTOR_INFO = {
    "name": "Pecuária",
    "icon": "🐄",
    "description": "Dejetos animais e resíduos pecuários",
    "color": "#ea580c",
    "gradient": "linear-gradient(135deg, #fed7aa 0%, #fdba74 100%)",
    "border_color": "#ea580c",
    "residues": list(PECUARIA_RESIDUES.keys())
}

__all__ = [
    'PECUARIA_RESIDUES',
    'PECUARIA_SECTOR_INFO',
    'DEJETO_DE_AVES_CAMA_DE_FRANGO_DATA',
    'DEJETO_DE_CODORNAS_DATA',
    'DEJETOS_DE_BOVINOS_LEITE__CORTE_DATA',
    'DEJETOS_DE_SUINOS_DATA',
]
