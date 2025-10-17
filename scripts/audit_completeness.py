#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 5 Completeness Audit - Compare 30 Validated Residues vs Database
Generates audit table showing which residues are in database and which are missing
"""

import sys
from pathlib import Path

# Fix encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.phase_5_saf_data import SAF_VALIDATION_DATA
from src.data.residue_registry import RESIDUES_REGISTRY

def run_completeness_audit():
    """Run completeness audit comparing validated 30 residues vs database"""

    print("=" * 120)
    print("PHASE 5: COMPLETENESS AUDIT - 30 VALIDATED RESIDUES vs DATABASE")
    print("=" * 120)
    print()

    # Get validated residues
    validated = list(SAF_VALIDATION_DATA.keys())
    validated_count = len(set(r for r in validated if not r.endswith(('(Leite)', '(Derivados)'))))  # Avoid duplicates

    # Get database residues
    in_database = list(RESIDUES_REGISTRY.keys())

    print(f"Total validated residues: {len(set(validated))}")
    print(f"Total in database: {len(in_database)}")
    print()
    print("=" * 120)
    print("AUDIT TABLE - ALL 30 VALIDATED RESIDUES")
    print("=" * 120)
    print()

    # Create audit table
    print("| Rank | Residue Name | SAF % | Priority Tier | In Database? | Status | Notes |")
    print("|------|--------------|-------|---------------|--------------|--------|-------|")

    missing_residues = []
    found_residues = []

    # Track unique residues (avoid listing variants like Soro Leite/Derivados separately)
    processed = set()

    for i, (residue, data) in enumerate(sorted(SAF_VALIDATION_DATA.items(), key=lambda x: x[1].get('saf_rank', 999)), 1):
        # Skip variants (keep only primary)
        base_name = residue.replace(' (Leite)', '').replace(' (Derivados)', '')
        if base_name in processed:
            continue
        processed.add(base_name)

        saf = data.get("saf_real", 0)
        tier = data.get("priority_tier", "UNKNOWN")
        rank = data.get("saf_rank", i)

        # Check if in database (exact or similar match)
        in_db = False
        match_name = ""
        for db_residue in in_database:
            if residue.lower() in db_residue.lower() or db_residue.lower() in residue.lower() or base_name.lower() in db_residue.lower():
                in_db = True
                match_name = db_residue
                break

        status = "✓ PRESENT" if in_db else "✗ MISSING"
        color_code = "✓" if in_db else "✗"

        if in_db:
            found_residues.append(residue)
        else:
            missing_residues.append((rank, residue, saf, tier))

        print(f"| {rank:2} | {residue:<30} | {saf:5.2f}% | {tier:<13} | {color_code} {in_db:5} | {status:<12} | {match_name if in_db else 'NOT FOUND':<30} |")

    print()
    print("=" * 120)
    print("SUMMARY")
    print("=" * 120)
    print(f"Total unique validated residues: {len(processed)}")
    print(f"Found in database: {len(found_residues)}")
    print(f"Missing from database: {len(missing_residues)}")
    print(f"Coverage: {len(found_residues) / len(processed) * 100:.1f}%")
    print()

    if missing_residues:
        print("=" * 120)
        print("MISSING RESIDUES (Priority Order)")
        print("=" * 120)
        print()
        print("| Rank | Residue Name | SAF % | Priority Tier | Action |")
        print("|------|--------------|-------|---------------|--------|")

        for rank, residue, saf, tier in sorted(missing_residues, key=lambda x: x[0]):
            print(f"| {rank:2} | {residue:<30} | {saf:5.2f}% | {tier:<13} | CREATE FILE |")

        print()
        print(f"ACTION: Create {len(missing_residues)} missing residue files")
        print()

    return len(processed), len(found_residues), len(missing_residues)

if __name__ == "__main__":
    total, found, missing = run_completeness_audit()
    print(f"\nAudit complete: {found}/{total} residues in database ({found/total*100:.1f}%)")
