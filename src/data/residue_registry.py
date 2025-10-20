"""
Central Residue Registry - SOLID Architecture
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Central registry for all residues across all sectors
Provides backward-compatible API with the old research_data.py

Open/Closed Principle: Easy to add new sectors/residues without modifying existing code

UPDATED: Now loads data from cp2b_panorama.db instead of hardcoded files
"""

from typing import Dict, List, Optional
from src.models.residue_models import ResidueData

# NOVO: Importar loader do banco de dados
try:
    from src.data.database_loader import load_all_residues_from_db
    USE_DATABASE = True
except ImportError:
    USE_DATABASE = False
    print("AVISO: database_loader não disponível, usando dados hardcoded")

# ============================================================================
# UNIFIED REGISTRY
# ============================================================================

# Carregar do banco de dados se disponível, senão usar hardcoded
RESIDUES_REGISTRY: Dict[str, ResidueData] = {}

if USE_DATABASE:
    try:
        RESIDUES_REGISTRY = load_all_residues_from_db()
        print(f"[OK] Carregados {len(RESIDUES_REGISTRY)} residuos do banco de dados")
    except Exception as e:
        print(f"[AVISO] Erro ao carregar banco, usando dados hardcoded: {e}")
        USE_DATABASE = False

# Fallback: Import all sector registries (se banco falhou ou não disponível)
if not USE_DATABASE:
    from src.data.agricultura import AGRICULTURA_RESIDUES, AGRICULTURA_SECTOR_INFO
    from src.data.pecuaria import PECUARIA_RESIDUES, PECUARIA_SECTOR_INFO
    from src.data.urbano import URBANO_RESIDUES, URBANO_SECTOR_INFO
    from src.data.industrial import INDUSTRIAL_RESIDUES, INDUSTRIAL_SECTOR_INFO
    
    # Fallback para dados hardcoded
    RESIDUES_REGISTRY = {
        **AGRICULTURA_RESIDUES,
        **PECUARIA_RESIDUES,
        **URBANO_RESIDUES,
        **INDUSTRIAL_RESIDUES,
    }

# Category organization - dinamicamente do registro
def _build_categories():
    """Constrói categorias dinamicamente a partir do registro"""
    cats = {}
    for name, residue in RESIDUES_REGISTRY.items():
        category = residue.category
        if category not in cats:
            cats[category] = []
        cats[category].append(name)
    return cats

CATEGORIES = _build_categories()

# Sector organization (new parallel structure)
if USE_DATABASE:
    # Mapeamento de códigos do banco para nomes amigáveis
    SECTOR_MAPPING = {
        'AG_AGRICULTURA': 'Agricultura',
        'PC_PECUARIA': 'Pecuária',
        'UR_URBANO': 'Urbano',
        'IN_INDUSTRIAL': 'Industrial'
    }
    
    SECTOR_ICONS = {
        'Agricultura': '🌾',
        'Pecuária': '🐄',
        'Urbano': '🏙️',
        'Industrial': '🏭'
    }
    
    # Organizar por setor do banco
    def _build_sectors():
        sectors = {}
        for name, residue in RESIDUES_REGISTRY.items():
            setor_code = getattr(residue, 'setor', None)
            if setor_code and setor_code in SECTOR_MAPPING:
                setor_name = SECTOR_MAPPING[setor_code]
                if setor_name not in sectors:
                    sectors[setor_name] = {
                        'name': setor_name,
                        'icon': SECTOR_ICONS.get(setor_name, '📊'),
                        'residues': []
                    }
                sectors[setor_name]['residues'].append(name)
        return sectors
    SECTORS = _build_sectors()
else:
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
