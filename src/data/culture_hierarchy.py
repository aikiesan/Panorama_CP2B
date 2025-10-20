"""
Culture Hierarchy Mapping - Phase 5
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Hierarchical organization: Sector -> Culture -> Residues
Provides 3-level selector support
"""

from typing import Dict, List, Optional

# ==============================================================================
# CULTURE METADATA
# ==============================================================================

# Culture metadata with icons and descriptions
CULTURE_METADATA = {
    # Agricultura
    "Cana-de-Açúcar": {
        "icon": "🍶",
        "description": "Resíduos da produção de cana-de-açúcar",
        "sector": "Agricultura",
    },
    "Citros": {
        "icon": "🍊",
        "description": "Resíduos da produção de citros",
        "sector": "Agricultura",
    },
    "Café": {
        "icon": "☕",
        "description": "Resíduos da produção de café",
        "sector": "Agricultura",
    },
    "Milho": {
        "icon": "🌽",
        "description": "Resíduos da produção de milho",
        "sector": "Agricultura",
    },
    "Soja": {
        "icon": "🫘",
        "description": "Resíduos da produção de soja",
        "sector": "Agricultura",
    },
    "Silvicultura": {
        "icon": "🌳",
        "description": "Resíduos de silvicultura e colheita florestal",
        "sector": "Agricultura",
    },
    "Cervejaria": {
        "icon": "🍺",
        "description": "Resíduos de produção de cerveja",
        "sector": "Agricultura",
    },
    # Pecuária
    "Avicultura": {
        "icon": "🐔",
        "description": "Resíduos de criação de aves",
        "sector": "Pecuária",
    },
    "Bovinocultura": {
        "icon": "🐄",
        "description": "Resíduos de criação de gado bovino",
        "sector": "Pecuária",
    },
    "Suinocultura": {
        "icon": "🐷",
        "description": "Resíduos de criação de suínos",
        "sector": "Pecuária",
    },
    "Piscicultura": {
        "icon": "🐟",
        "description": "Resíduos de criação de peixes",
        "sector": "Pecuária",
    },
}


# ==============================================================================
# HIERARCHICAL MAPPING: SECTOR -> CULTURE -> RESIDUES
# ==============================================================================

SECTOR_CULTURE_MAPPING = {
    "Agricultura": {
        "Cana-de-Açúcar": [
            "Bagaço de cana",
            "Torta de Filtro (Filter Cake)",
            "Vinhaça de Cana-de-açúcar",
            "Palha de Cana-de-açúcar (Palhiço)",
        ],
        "Citros": [
            "Cascas de citros",
            "Bagaço de citros",
        ],
        "Café": [
            "Mucilagem fermentada",
            "Casca de café (pergaminho)",
        ],
        "Milho": [
            "Sabugo de milho",
            "Palha de milho",
        ],
        "Soja": [
            "Vagens vazias",
            "Palha de soja",
        ],
        "Silvicultura": [
            "Casca de eucalipto",
            "Resíduos de colheita",
        ],
        "Cervejaria": [
            "Bagaço de malte",
        ],
    },
    "Pecuária": {
        "Avicultura": [
            "Cama de frango",
            "Dejeto de Aves (Cama de Frango)",
            "Dejetos de postura",
            "Dejeto de Codornas",
        ],
        "Bovinocultura": [
            "Cama de curral",
            "Dejetos de Bovinos (Leite + Corte)",
            "Dejetos bovinos",
            "Conteúdo ruminal",
            "Sangue bovino",
        ],
        "Suinocultura": [
            "Dejetos suínos",
            "Lodo de lagoas",
        ],
        "Piscicultura": [
            "Ração não consumida",
            "Lodo de tanques",
        ],
    },
}


# ==============================================================================
# PUBLIC API - Culture Hierarchy (3-Level: Sector -> Culture -> Residue)
# ==============================================================================

def get_cultures_by_sector(sector_name: str) -> List[str]:
    """
    Get list of cultures for a specific sector.

    Args:
        sector_name: Name of the sector ("Agricultura", "Pecuária", etc.)

    Returns:
        List of culture names (e.g., ["Cana-de-Açúcar", "Citros", ...])
    """
    return list(SECTOR_CULTURE_MAPPING.get(sector_name, {}).keys())


def get_culture_metadata(culture_name: str) -> Optional[Dict]:
    """
    Get metadata for a specific culture.

    Args:
        culture_name: Name of the culture (e.g., "Cana-de-Açúcar")

    Returns:
        Dictionary with icon, description, and sector
    """
    return CULTURE_METADATA.get(culture_name)


def get_residues_by_culture(sector_name: str, culture_name: str) -> List[str]:
    """
    Get list of residues for a specific culture within a sector.

    Args:
        sector_name: Name of the sector
        culture_name: Name of the culture

    Returns:
        List of residue names
    """
    sector_cultures = SECTOR_CULTURE_MAPPING.get(sector_name, {})
    return sector_cultures.get(culture_name, [])


def get_culture_icon(culture_name: str) -> str:
    """
    Get emoji icon for a specific culture.

    Args:
        culture_name: Name of the culture

    Returns:
        Emoji icon string
    """
    metadata = CULTURE_METADATA.get(culture_name, {})
    return metadata.get("icon", "📊")


def get_all_cultures() -> List[str]:
    """
    Get list of all culture names across all sectors.

    Returns:
        List of all culture names
    """
    return list(CULTURE_METADATA.keys())


__all__ = [
    'CULTURE_METADATA',
    'SECTOR_CULTURE_MAPPING',
    'get_cultures_by_sector',
    'get_culture_metadata',
    'get_residues_by_culture',
    'get_culture_icon',
    'get_all_cultures',
]
