"""
FDE Helper Utilities - Phase 5
Utilities for working with FDE (Fator de Disponibilidade Efetiva) data in UI and calculations
"""

from typing import Dict, List, Tuple, Optional
from src.data.phase_5_fde_data import FDE_VALIDATION_DATA

# Priority tier color mapping for UI
PRIORITY_COLORS = {
    "EXCEPCIONAL": "#d946ef",  # Purple - Highest
    "EXCELENTE": "#0891b2",    # Cyan
    "MUITO BOM": "#059669",    # Green
    "BOM": "#0d9488",          # Teal
    "RAZOÁVEL": "#f59e0b",     # Amber
    "REGULAR": "#f97316",      # Orange
    "BAIXO": "#dc2626",        # Red
    "CRÍTICO": "#7c2d12",      # Dark Red
    "INVIÁVEL": "#6b7280",     # Gray
}

# Priority tier emoji mapping
PRIORITY_EMOJI = {
    "EXCEPCIONAL": "🏆",
    "EXCELENTE": "⭐",
    "MUITO BOM": "✅",
    "BOM": "👍",
    "RAZOÁVEL": "⚠️",
    "REGULAR": "📊",
    "BAIXO": "❌",
    "CRÍTICO": "🚫",
    "INVIÁVEL": "⛔",
}

def get_fde_tier_color(priority_tier: str) -> str:
    """Get color for priority tier"""
    return PRIORITY_COLORS.get(priority_tier, "#9ca3af")

def get_fde_tier_emoji(priority_tier: str) -> str:
    """Get emoji for priority tier"""
    return PRIORITY_EMOJI.get(priority_tier, "📊")

def filter_residues_by_fde_threshold(residues: List[str], min_fde: float = 0.0, max_fde: float = 100.0) -> List[str]:
    """
    Filter residues by FDE range

    Args:
        residues: List of residue names
        min_fde: Minimum FDE percentage
        max_fde: Maximum FDE percentage

    Returns:
        Filtered list of residues
    """
    filtered = []
    for residue in residues:
        fde_data = FDE_VALIDATION_DATA.get(residue)
        if fde_data:
            fde = fde_data.get("fde_real", 0)
            if min_fde <= fde <= max_fde:
                filtered.append(residue)
        # Include residues not in FDE analysis
        else:
            filtered.append(residue)
    return filtered

def sort_residues_by_fde(residues: List[str], descending: bool = True) -> List[str]:
    """
    Sort residues by FDE value

    Args:
        residues: List of residue names
        descending: Sort descending (highest first) if True

    Returns:
        Sorted list of residues
    """
    def get_fde(residue):
        fde_data = FDE_VALIDATION_DATA.get(residue)
        return fde_data.get("fde_real", -1) if fde_data else -1

    return sorted(residues, key=get_fde, reverse=descending)

def get_priority_tier_for_residue(residue: str) -> Optional[str]:
    """Get priority tier for a residue"""
    fde_data = FDE_VALIDATION_DATA.get(residue)
    if fde_data:
        return fde_data.get("priority_tier")
    return None

def get_fde_real_for_residue(residue: str) -> Optional[float]:
    """Get FDE real value for a residue"""
    fde_data = FDE_VALIDATION_DATA.get(residue)
    if fde_data:
        return fde_data.get("fde_real")
    return None

def get_recommendation_for_residue(residue: str) -> Optional[str]:
    """Get recommendation for a residue"""
    fde_data = FDE_VALIDATION_DATA.get(residue)
    if fde_data:
        return fde_data.get("recommendation")
    return None

def get_culture_for_residue(residue: str) -> Optional[str]:
    """Get culture group for a residue"""
    fde_data = FDE_VALIDATION_DATA.get(residue)
    if fde_data:
        return fde_data.get("culture_group")
    return None

def get_residues_by_tier(tier: str) -> List[str]:
    """Get all residues of a specific priority tier"""
    return [
        name for name, data in FDE_VALIDATION_DATA.items()
        if data.get("priority_tier") == tier
    ]

def get_high_priority_residues(threshold: float = 8.0) -> List[str]:
    """Get all high-priority residues (FDE > threshold)"""
    return [
        name for name, data in FDE_VALIDATION_DATA.items()
        if data.get("fde_real", 0) >= threshold
    ]

def get_viable_residues(threshold: float = 4.0) -> List[str]:
    """Get all viable residues (FDE > threshold)"""
    return [
        name for name, data in FDE_VALIDATION_DATA.items()
        if data.get("fde_real", 0) >= threshold
    ]

def get_low_priority_residues(threshold: float = 1.0) -> List[str]:
    """Get all low-priority residues (FDE < threshold)"""
    return [
        name for name, data in FDE_VALIDATION_DATA.items()
        if data.get("fde_real", 0) < threshold
    ]

def create_fde_badge(residue: str) -> str:
    """Create a formatted FDE badge for display"""
    fde_data = FDE_VALIDATION_DATA.get(residue)
    if not fde_data:
        return "⏭️ Not analyzed"

    tier = fde_data.get("priority_tier", "UNKNOWN")
    fde_val = fde_data.get("fde_real", 0)
    emoji = get_fde_tier_emoji(tier)

    return f"{emoji} {tier} ({fde_val:.2f}%)"

def get_fde_factors(residue: str) -> Optional[Dict[str, float]]:
    """Get FDE factor breakdown for a residue"""
    fde_data = FDE_VALIDATION_DATA.get(residue)
    if not fde_data:
        return None

    return {
        "FC (Coleta)": fde_data.get("fc", 0),
        "FCp (Competição)": fde_data.get("fcp", 0),
        "FS (Sazonalidade)": fde_data.get("fs", 0),
        "FL (Logístico)": fde_data.get("fl", 0),
    }

def calculate_fde_from_factors(fc: float, fcp: float, fs: float, fl: float) -> float:
    """Calculate FDE from individual factors"""
    # FDE_REAL = FC × (1/FCp) × FS × FL
    return fc * (1 / fcp) * fs * fl if fcp > 0 else 0

def get_residues_ranking() -> List[Tuple[str, float, str, int]]:
    """Get all residues ranked by FDE"""
    ranking = []
    for residue, data in FDE_VALIDATION_DATA.items():
        ranking.append((
            residue,
            data.get("fde_real", 0),
            data.get("priority_tier", "UNKNOWN"),
            data.get("fde_rank", 999)
        ))

    # Sort by rank
    return sorted(ranking, key=lambda x: x[3])

if __name__ == "__main__":
    # Test
    print("FDE Helpers Test")
    print(f"High-priority residues (FDE > 8%): {get_high_priority_residues()}")
    print(f"Viable residues (FDE > 4%): {len(get_viable_residues())} total")
    print(f"Top 5 residues: {[r[0] for r in get_residues_ranking()[:5]]}")
