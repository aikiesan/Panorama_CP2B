#!/usr/bin/env python3
"""
Batch SAF Application Script - Phase 5
Applies SAF validation data to all residues automatically
Usage: python scripts/apply_saf_batch.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.phase_5_saf_data import SAF_VALIDATION_DATA, get_residues_by_priority

def apply_saf_to_residues_in_registry():
    """Apply SAF data to all residues in registry"""
    from src.data.residue_registry import RESIDUES_REGISTRY
    from src.data.phase_5_saf_data import apply_saf_to_residue

    applied_count = 0
    skipped_count = 0

    print("=" * 70)
    print("PHASE 5: Batch SAF Application")
    print("=" * 70)

    for residue_name, residue_data in RESIDUES_REGISTRY.items():
        saf_data = SAF_VALIDATION_DATA.get(residue_name)

        if saf_data:
            apply_saf_to_residue(residue_data, residue_name)
            applied_count += 1
            print(f"✅ {residue_name:<45} | SAF: {saf_data['saf_real']:.2f}% | Rank: {saf_data['saf_rank']}")
        else:
            skipped_count += 1
            # Uncomment to see which residues are not in SAF analysis
            # print(f"⏭️  {residue_name:<45} | (Not in SAF analysis)")

    print("\n" + "=" * 70)
    print(f"RESULTS:")
    print(f"  Applied: {applied_count}/29 residues from SAF analysis")
    print(f"  Skipped: {skipped_count} residues (not in SAF analysis)")
    print(f"  Total in registry: {applied_count + skipped_count}")
    print("=" * 70)

    # Summary by priority tier
    print("\nSUMMARY BY PRIORITY TIER:")
    tiers = ["EXCEPCIONAL", "EXCELENTE", "MUITO BOM", "BOM", "RAZOÁVEL", "REGULAR", "BAIXO", "CRÍTICO", "INVIÁVEL"]

    for tier in tiers:
        residues = get_residues_by_priority(tier)
        if residues:
            print(f"  {tier:<15} ({len(residues):2} residues)")

if __name__ == "__main__":
    apply_saf_to_residues_in_registry()
