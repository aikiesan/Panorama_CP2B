"""
Central Residue Registry - SOLID Architecture
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Central registry for all residues across all sectors
Provides backward-compatible API with the old research_data.py

Open/Closed Principle: Easy to add new sectors/residues without modifying existing code
"""

from typing import Dict, List, Optional
from src.models.residue_models import ResidueData

# Import all sector registries
from src.data.agricultura import AGRICULTURA_RESIDUES, AGRICULTURA_SECTOR_INFO
from src.data.pecuaria import PECUARIA_RESIDUES, PECUARIA_SECTOR_INFO
from src.data.urbano import URBANO_RESIDUES, URBANO_SECTOR_INFO
from src.data.industrial import INDUSTRIAL_RESIDUES, INDUSTRIAL_SECTOR_INFO


# ============================================================================
# UNIFIED REGISTRIES
# ============================================================================

# All residues across all sectors
RESIDUES_REGISTRY: Dict[str, ResidueData] = {
    **AGRICULTURA_RESIDUES,
    **PECUARIA_RESIDUES,
    **URBANO_RESIDUES,
    **INDUSTRIAL_RESIDUES,
}

# Category organization (old structure - backward compatibility)
CATEGORIES = {
    "Agricultura": list(AGRICULTURA_RESIDUES.keys()),
    "Pecuária": list(PECUARIA_RESIDUES.keys()),
    "Urbano": list(URBANO_RESIDUES.keys()),
    "Industrial": list(INDUSTRIAL_RESIDUES.keys()),
}

# Sector organization (new parallel structure)
SECTORS = {
    "Agricultura": AGRICULTURA_SECTOR_INFO,
    "Pecuária": PECUARIA_SECTOR_INFO,
    "Urbano": URBANO_SECTOR_INFO,
    "Industrial": INDUSTRIAL_SECTOR_INFO,
}


# ============================================================================
# PUBLIC API - Backward Compatible
# ============================================================================

def get_available_residues() -> List[str]:
    """Get list of all available residues"""
    return list(RESIDUES_REGISTRY.keys())


def get_residue_data(residue_name: str) -> Optional[ResidueData]:
    """Get complete data for a specific residue"""
    return RESIDUES_REGISTRY.get(residue_name)


def get_residues_by_category(category: str) -> List[str]:
    """Get list of residues by category (backward compatibility)"""
    return CATEGORIES.get(category, [])


def get_category_icon(category: str) -> str:
    """Get emoji icon for category (backward compatibility)"""
    icons = {
        "Agricultura": "🌾",
        "Pecuária": "🐄",
        "Urbano": "🏙️",
        "Industrial": "🏭",
    }
    return icons.get(category, "📊")


def get_residue_icon(residue_name: str) -> str:
    """Get emoji icon for specific residue"""
    residue = get_residue_data(residue_name)
    return residue.icon if residue else "📊"


# ============================================================================
# NEW API - Sector-based
# ============================================================================

def get_all_sectors() -> Dict[str, Dict]:
    """Get all parallel sectors with metadata"""
    return SECTORS


def get_sector_info(sector_name: str) -> Optional[Dict]:
    """Get metadata for a specific sector"""
    return SECTORS.get(sector_name)


def get_residues_by_sector(sector_name: str) -> List[str]:
    """Get list of residues for a specific parallel sector"""
    sector = SECTORS.get(sector_name)
    return sector.get("residues", []) if sector else []


def get_available_sectors() -> List[str]:
    """Get list of sector names with available residues"""
    return [name for name, info in SECTORS.items() if info.get("residues")]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def parse_range_from_string(value_str: str) -> Optional[object]:
    """
    Parse range from string like "Range: 200-350" or "range: 70-80%"
    (Placeholder - implement if needed)
    """
    import re
    from src.models.residue_models import ParameterRange

    # Pattern to match "Range: min-max" or "range: min-max"
    pattern = r'[Rr]ange[:\s]+(\d+\.?\d*)\s*-\s*(\d+\.?\d*)'
    match = re.search(pattern, value_str)

    if match:
        min_val = float(match.group(1))
        max_val = float(match.group(2))
        mean_val = (min_val + max_val) / 2

        # Extract unit if present
        unit_pattern = r'%|L|kg|m³|mg/L|g/L|°C|dias?|days?'
        unit_match = re.search(unit_pattern, value_str)
        unit = unit_match.group(0) if unit_match else None

        return ParameterRange(min=min_val, mean=mean_val, max=max_val, unit=unit)

    return None


# ============================================================================
# MODULE INFO
# ============================================================================

__all__ = [
    # Registries
    'RESIDUES_REGISTRY',
    'CATEGORIES',
    'SECTORS',

    # Backward-compatible API
    'get_available_residues',
    'get_residue_data',
    'get_residues_by_category',
    'get_category_icon',
    'get_residue_icon',

    # New sector-based API
    'get_all_sectors',
    'get_sector_info',
    'get_residues_by_sector',
    'get_available_sectors',

    # Utilities
    'parse_range_from_string',
]
