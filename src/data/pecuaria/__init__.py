"""
Pecuária Sector Registry
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Register all livestock residues
"""

from .avicultura_frango import DEJETO_DE_AVES_CAMA_DE_FRANGO_DATA
from .avicultura_codornas import DEJETO_DE_CODORNAS_DATA
from .bovinocultura import DEJETOS_DE_BOVINOS_LEITE__CORTE_DATA
from .suinocultura import DEJETOS_DE_SUINOS_DATA
from .dejetos_bovinos import DEJETOS_BOVINOS_DATA
from .lodo_de_tanques import LODO_DE_TANQUES_DATA

# Import residues moved from agricultura sector for proper sector organization
from ..agricultura.cama_de_frango import CAMA_DE_FRANGO_DATA
from ..agricultura.cama_de_curral import CAMA_DE_CURRAL_DATA
from ..agricultura.dejetos_de_postura import DEJETOS_DE_POSTURA_DATA
from ..agricultura.dejetos_suínos import DEJETOS_SUÍNOS_DATA
from ..agricultura.conteúdo_ruminal import CONTEÚDO_RUMINAL_DATA
from ..agricultura.sangue_bovino import SANGUE_BOVINO_DATA
from ..agricultura.ração_não_consumida import RAÇÃO_NÃO_CONSUMIDA_DATA
from ..agricultura.lodo_de_lagoas import LODO_DE_LAGOAS_DATA

# Registry of all pecuaria residues
PECUARIA_RESIDUES = {
    # ===== AVICULTURA (Poultry) =====
    "Cama de frango": CAMA_DE_FRANGO_DATA,
    "Dejeto de Aves (Cama de Frango)": DEJETO_DE_AVES_CAMA_DE_FRANGO_DATA,
    "Dejetos de postura": DEJETOS_DE_POSTURA_DATA,
    "Dejeto de Codornas": DEJETO_DE_CODORNAS_DATA,

    # ===== BOVINOCULTURA (Cattle) =====
    "Cama de curral": CAMA_DE_CURRAL_DATA,
    "Dejetos de Bovinos (Leite + Corte)": DEJETOS_DE_BOVINOS_LEITE__CORTE_DATA,
    "Dejetos bovinos": DEJETOS_BOVINOS_DATA,
    "Conteúdo ruminal": CONTEÚDO_RUMINAL_DATA,
    "Sangue bovino": SANGUE_BOVINO_DATA,

    # ===== SUINOCULTURA (Swine) =====
    "Dejetos suínos": DEJETOS_SUÍNOS_DATA,
    "Lodo de lagoas": LODO_DE_LAGOAS_DATA,

    # ===== PISCICULTURA (Aquaculture) =====
    "Ração não consumida": RAÇÃO_NÃO_CONSUMIDA_DATA,
    "Lodo de tanques": LODO_DE_TANQUES_DATA,
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
