#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply SAF to all residues in the registry
This script programmatically applies SAF validation data to all residues
"""

import sys
import io
from pathlib import Path

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.residue_registry import RESIDUES_REGISTRY
from src.data.phase_5_saf_data import SAF_VALIDATION_DATA

def apply_saf_to_all():
    """Apply SAF data to all residues in registry"""
    applied = 0
    not_found = 0

    print("=" * 80)
    print("PHASE 5: Applying SAF to All Residues in Registry")
    print("=" * 80)
    print()

    for residue_name, residue_data in RESIDUES_REGISTRY.items():
        saf_data = SAF_VALIDATION_DATA.get(residue_name)

        if saf_data:
            # Apply SAF fields
            residue_data.saf_real = saf_data.get("saf_real")
            residue_data.priority_tier = saf_data.get("priority_tier")
            residue_data.saf_rank = saf_data.get("saf_rank")
            residue_data.recommendation = saf_data.get("recommendation")
            residue_data.fc_value = saf_data.get("fc")
            residue_data.fcp_value = saf_data.get("fcp")
            residue_data.fs_value = saf_data.get("fs")
            residue_data.fl_value = saf_data.get("fl")
            residue_data.culture_group = saf_data.get("culture_group")

            applied += 1
            saf_val = saf_data.get("saf_real", 0)
            tier = saf_data.get("priority_tier", "UNKNOWN")
            print(f"✅ {residue_name:<45} | SAF: {saf_val:6.2f}% | {tier:<15}")
        else:
            not_found += 1
            print(f"⏭️  {residue_name:<45} | (Not in SAF analysis)")

    print()
    print("=" * 80)
    print(f"RESULTS:")
    print(f"  ✅ Applied to:        {applied} residues")
    print(f"  ⏭️  Not in SAF data:    {not_found} residues")
    print(f"  📊 Total in registry: {applied + not_found} residues")
    print("=" * 80)
    print()

    # Summary by priority tier
    print("SUMMARY BY PRIORITY TIER:")
    tiers = ["EXCEPCIONAL", "EXCELENTE", "MUITO BOM", "BOM", "RAZOÁVEL", "REGULAR", "BAIXO", "CRÍTICO", "INVIÁVEL"]

    tier_counts = {}
    for tier in tiers:
        count = sum(1 for data in SAF_VALIDATION_DATA.values() if data.get("priority_tier") == tier)
        if count > 0:
            tier_counts[tier] = count
            print(f"  {tier:<15} : {count:2} residues")

    print()
    print("=" * 80)
    print(f"HIGH-PRIORITY OPPORTUNITIES (SAF > 8%):")
    high_priority = [
        (name, data.get("saf_real"), data.get("priority_tier"))
        for name, data in SAF_VALIDATION_DATA.items()
        if data.get("saf_real", 0) >= 8.0
    ]
    high_priority.sort(key=lambda x: x[1], reverse=True)

    for name, saf, tier in high_priority:
        print(f"  🔥 {name:<40} | SAF: {saf:6.2f}% | {tier}")

    return applied, not_found

if __name__ == "__main__":
    applied, not_found = apply_saf_to_all()
    print()
    print(f"SUCCESS: Applied SAF to {applied} residues")
    print(f"NOTE: {not_found} residues are not yet in the validated SAF analysis")
