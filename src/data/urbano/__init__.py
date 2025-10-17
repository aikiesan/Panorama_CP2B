"""
Urbano Sector Registry
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Register all urban residues
"""

from .rsu import RSU_DATA
from .rpo import RPO_DATA
from .lodo import LODO_ETE_DATA
from .galhos_e_folhas import GALHOS_E_FOLHAS_DATA

# Import residues moved from agricultura sector for proper sector organization
from ..agricultura.grama_cortada import GRAMA_CORTADA_DATA

# Registry of all urbano residues
URBANO_RESIDUES = {
    "RSU - Resíduo Sólido Urbano": RSU_DATA,
    "RPO - Poda Urbana": RPO_DATA,
    "Lodo de Esgoto (ETE)": LODO_ETE_DATA,
    "Galhos e folhas": GALHOS_E_FOLHAS_DATA,
    "Grama cortada": GRAMA_CORTADA_DATA,
}

# Sector metadata
URBANO_SECTOR_INFO = {
    "name": "Urbano",
    "icon": "🏙️",
    "description": "Resíduos sólidos urbanos, poda urbana e lodo de esgoto",
    "color": "#7c3aed",
    "gradient": "linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%)",
    "border_color": "#7c3aed",
    "residues": list(URBANO_RESIDUES.keys())
}

__all__ = [
    'URBANO_RESIDUES',
    'URBANO_SECTOR_INFO',
    'RSU_DATA',
    'RPO_DATA',
    'LODO_ETE_DATA',
]
