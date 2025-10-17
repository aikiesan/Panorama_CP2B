"""
SAF Helper Utilities - Phase 5
Utilities for working with SAF data in UI and calculations
"""

from typing import Dict, List, Tuple, Optional
from src.data.phase_5_saf_data import SAF_VALIDATION_DATA

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

def get_saf_tier_color(priority_tier: str) -> str:
    """Get color for priority tier"""
    return PRIORITY_COLORS.get(priority_tier, "#9ca3af")

def get_saf_tier_emoji(priority_tier: str) -> str:
    """Get emoji for priority tier"""
    return PRIORITY_EMOJI.get(priority_tier, "📊")

def filter_residues_by_saf_threshold(residues: List[str], min_saf: float = 0.0, max_saf: float = 100.0) -> List[str]:
    """
    Filter residues by SAF range

    Args:
        residues: List of residue names
        min_saf: Minimum SAF percentage
        max_saf: Maximum SAF percentage

    Returns:
        Filtered list of residues
    """
    filtered = []
    for residue in residues:
        saf_data = SAF_VALIDATION_DATA.get(residue)
        if saf_data:
            saf = saf_data.get("saf_real", 0)
            if min_saf <= saf <= max_saf:
                filtered.append(residue)
        # Include residues not in SAF analysis
        else:
            filtered.append(residue)
    return filtered

def sort_residues_by_saf(residues: List[str], descending: bool = True) -> List[str]:
    """
    Sort residues by SAF value

    Args:
        residues: List of residue names
        descending: Sort descending (highest first) if True

    Returns:
        Sorted list of residues
    """
    def get_saf(residue):
        saf_data = SAF_VALIDATION_DATA.get(residue)
        return saf_data.get("saf_real", -1) if saf_data else -1

    return sorted(residues, key=get_saf, reverse=descending)

def get_priority_tier_for_residue(residue: str) -> Optional[str]:
    """Get priority tier for a residue"""
    saf_data = SAF_VALIDATION_DATA.get(residue)
    if saf_data:
        return saf_data.get("priority_tier")
    return None

def get_saf_real_for_residue(residue: str) -> Optional[float]:
    """Get SAF real value for a residue"""
    saf_data = SAF_VALIDATION_DATA.get(residue)
    if saf_data:
        return saf_data.get("saf_real")
    return None

def get_recommendation_for_residue(residue: str) -> Optional[str]:
    """Get recommendation for a residue"""
    saf_data = SAF_VALIDATION_DATA.get(residue)
    if saf_data:
        return saf_data.get("recommendation")
    return None

def get_culture_for_residue(residue: str) -> Optional[str]:
    """Get culture group for a residue"""
    saf_data = SAF_VALIDATION_DATA.get(residue)
    if saf_data:
        return saf_data.get("culture_group")
    return None

def get_residues_by_tier(tier: str) -> List[str]:
    """Get all residues of a specific priority tier"""
    return [
        name for name, data in SAF_VALIDATION_DATA.items()
        if data.get("priority_tier") == tier
    ]

def get_high_priority_residues(threshold: float = 8.0) -> List[str]:
    """Get all high-priority residues (SAF > threshold)"""
    return [
        name for name, data in SAF_VALIDATION_DATA.items()
        if data.get("saf_real", 0) >= threshold
    ]

def get_viable_residues(threshold: float = 4.0) -> List[str]:
    """Get all viable residues (SAF > threshold)"""
    return [
        name for name, data in SAF_VALIDATION_DATA.items()
        if data.get("saf_real", 0) >= threshold
    ]

def get_low_priority_residues(threshold: float = 1.0) -> List[str]:
    """Get all low-priority residues (SAF < threshold)"""
    return [
        name for name, data in SAF_VALIDATION_DATA.items()
        if data.get("saf_real", 0) < threshold
    ]

def create_saf_badge(residue: str) -> str:
    """Create a formatted SAF badge for display"""
    saf_data = SAF_VALIDATION_DATA.get(residue)
    if not saf_data:
        return "⏭️ Not analyzed"

    tier = saf_data.get("priority_tier", "UNKNOWN")
    saf_val = saf_data.get("saf_real", 0)
    emoji = get_saf_tier_emoji(tier)

    return f"{emoji} {tier} ({saf_val:.2f}%)"

def get_saf_factors(residue: str) -> Optional[Dict[str, float]]:
    """Get SAF factor breakdown for a residue"""
    saf_data = SAF_VALIDATION_DATA.get(residue)
    if not saf_data:
        return None

    return {
        "FC (Coleta)": saf_data.get("fc", 0),
        "FCp (Competição)": saf_data.get("fcp", 0),
        "FS (Sazonalidade)": saf_data.get("fs", 0),
        "FL (Logístico)": saf_data.get("fl", 0),
    }

def calculate_saf_from_factors(fc: float, fcp: float, fs: float, fl: float) -> float:
    """Calculate SAF from individual factors"""
    # SAF_REAL = FC × (1/FCp) × FS × FL
    return fc * (1 / fcp) * fs * fl if fcp > 0 else 0

def get_residues_ranking() -> List[Tuple[str, float, str, int]]:
    """Get all residues ranked by SAF"""
    ranking = []
    for residue, data in SAF_VALIDATION_DATA.items():
        ranking.append((
            residue,
            data.get("saf_real", 0),
            data.get("priority_tier", "UNKNOWN"),
            data.get("saf_rank", 999)
        ))

    # Sort by rank
    return sorted(ranking, key=lambda x: x[3])

if __name__ == "__main__":
    # Test
    print("SAF Helpers Test")
    print(f"High-priority residues (SAF > 8%): {get_high_priority_residues()}")
    print(f"Viable residues (SAF > 4%): {len(get_viable_residues())} total")
    print(f"Top 5 residues: {[r[0] for r in get_residues_ranking()[:5]]}")
