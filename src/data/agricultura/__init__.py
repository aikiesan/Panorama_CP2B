"""
Agricultura Sector Registry
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Register all agriculture residues
"""

# Main sugar cane residues (original 3) - Hierarchical Structure by Culture
from .cana_vinhaca import VINHACA_DE_CANA_DE_ACUCAR_DATA
from .cana_palha import PALHA_DE_CANA_DE_ACUCAR_PALHICO_DATA
from .cana_torta import TORTA_DE_FILTRO_FILTER_CAKE_DATA
from .bagaço_de_cana import BAGAÇO_DE_CANA_DATA

# NOTE: Duplicate entries removed (Phase 5 restructuring):
# - "Palha de cana" → Use "Palha de Cana-de-açúcar (Palhiço)" instead
# - "Torta de filtro" → Use "Torta de Filtro (Filter Cake)" instead
# - "Vinhaça" → Use "Vinhaça de Cana-de-açúcar" instead
# - "Cana-de-açúcar" → Composite residue (see sub_residues)

# Citrus residues
from .bagaço_de_citros import BAGAÇO_DE_CITROS_DATA
from .cascas_de_citros import CASCAS_DE_CITROS_DATA

# Coffee residues
from .casca_de_café_pergaminho import CASCA_DE_CAFÉ_PERGAMINHO_DATA

# Other crop residues
from .palha_de_milho import PALHA_DE_MILHO_DATA
from .sabugo_de_milho import SABUGO_DE_MILHO_DATA
from .palha_de_soja import PALHA_DE_SOJA_DATA
from .vagens_vazias import VAGENS_VAZIAS_DATA
from .casca_de_eucalipto import CASCA_DE_EUCALIPTO_DATA
from .resíduos_de_colheita import RESÍDUOS_DE_COLHEITA_DATA

# Industrial/processing residues
from .bagaço_de_malte import BAGAÇO_DE_MALTE_DATA
from .mucilagem_fermentada import MUCILAGEM_FERMENTADA_DATA

# NOTE: Animal-related residues have been moved to src/data/pecuaria/
# NOTE: Urban/landscape residues have been moved to src/data/urbano/

# Registry of all agricultura residues
# Phase 5: Hierarchical organization by culture
# Cana-de-Açúcar group (4 residues):
CANA_DE_ACUCAR_RESIDUES = {
    "Vinhaça de Cana-de-açúcar": VINHACA_DE_CANA_DE_ACUCAR_DATA,
    "Palha de Cana-de-açúcar (Palhiço)": PALHA_DE_CANA_DE_ACUCAR_PALHICO_DATA,
    "Torta de Filtro (Filter Cake)": TORTA_DE_FILTRO_FILTER_CAKE_DATA,
    "Bagaço de cana": BAGAÇO_DE_CANA_DATA,
}

AGRICULTURA_RESIDUES = {
    # ===== CANA-DE-AÇÚCAR GROUP (4 residues - SAF ranking) =====
    # Rank 1: Bagaço de cana (80.75%) - EXCEPCIONAL
    # Rank 3: Torta de Filtro (12.88%) - MUITO BOM
    # Rank 5: Vinhaça (10.26%) - BOM
    # Rank 26: Palha (1.18%) - CRÍTICO (low priority)
    **CANA_DE_ACUCAR_RESIDUES,

    # ===== CITROS GROUP (2 residues - SAF ranking) =====
    # Rank 17: Cascas citros (3.26%) - REGULAR
    # Rank 20: Bagaço citros (2.33%) - BAIXO
    "Bagaço de citros": BAGAÇO_DE_CITROS_DATA,
    "Cascas de citros": CASCAS_DE_CITROS_DATA,

    # ===== CAFÉ GROUP (1 residue from Phase 4, need Mucilagem) =====
    # Note: Mucilagem fermentada (11.90%) - MUITO BOM - Should be added
    # Rank 18: Casca café (2.67%) - BAIXO
    "Casca de café (pergaminho)": CASCA_DE_CAFÉ_PERGAMINHO_DATA,
    # "Mucilagem fermentada": MUCILAGEM_FERMENTADA_DATA,  # Imported but not coffee - see below

    # ===== MILHO GROUP (2 residues - SAF ranking) =====
    # Rank 21: Sabugo milho (2.25%) - BAIXO
    # Rank 22: Palha milho (1.96%) - BAIXO
    "Palha de milho": PALHA_DE_MILHO_DATA,
    "Sabugo de milho": SABUGO_DE_MILHO_DATA,

    # ===== SOJA GROUP (2 residues - SAF ranking) =====
    # Rank 24: Vagens vazias (1.37%) - CRÍTICO
    # Rank 25: Palha soja (1.36%) - CRÍTICO
    "Palha de soja": PALHA_DE_SOJA_DATA,
    "Vagens vazias": VAGENS_VAZIAS_DATA,

    # ===== SILVICULTURA GROUP (2 residues - SAF ranking) =====
    # Rank 28: Casca eucalipto (0.95%) - INVIÁVEL
    # Rank 29: Resíduos colheita (0.74%) - INVIÁVEL
    "Casca de eucalipto": CASCA_DE_EUCALIPTO_DATA,
    "Resíduos de colheita": RESÍDUOS_DE_COLHEITA_DATA,

    # ===== INDUSTRIAL/PROCESSAMENTO (NOT agricultura but grouped here) =====
    # Rank 9: Bagaço malte (6.69%) - RAZOÁVEL
    # Rank 4: Mucilagem café (11.90%) - MUITO BOM (should be moved to Café group)
    "Bagaço de malte": BAGAÇO_DE_MALTE_DATA,
    "Mucilagem fermentada": MUCILAGEM_FERMENTADA_DATA,

    # ===== NOTE: ANIMAL RESIDUES MOVED TO PECUÁRIA =====
    # The following residues were previously here but have been moved to src/data/pecuaria:
    # - Cama de frango → Avicultura
    # - Cama de curral → Bovinocultura
    # - Dejetos de postura → Avicultura
    # - Dejetos suínos → Suinocultura
    # - Conteúdo ruminal → Frigorífico/Bovinocultura
    # - Sangue bovino → Frigorífico/Bovinocultura
    # - Ração não consumida → Piscicultura
    # - Lodo de lagoas → Suinocultura/Bovinocultura

    # ===== NOTE: URBANO RESIDUE MOVED TO URBANO =====
    # Grama cortada has been moved to src/data/urbano
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
