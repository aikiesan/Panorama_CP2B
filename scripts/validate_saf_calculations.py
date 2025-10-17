#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAF Validation Script - Phase 5
Validates that all SAF calculations are mathematically correct
and factor values are within specified ranges

Usage: python scripts/validate_saf_calculations.py
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

from src.data.phase_5_saf_data import SAF_VALIDATION_DATA


def calculate_saf_from_factors(fc, fcp, fs, fl):
    """Calculate SAF_REAL from individual factors using formula: FC × (1/FCp) × FS × FL"""
    if fcp <= 0:
        return 0
    return (fc * (1 / fcp) * fs * fl) * 100  # Multiply by 100 to get percentage


def validate_saf_calculations():
    """Validate all SAF calculations and factor ranges"""

    print("=" * 100)
    print("PHASE 5: SAF CALCULATION VALIDATION")
    print("=" * 100)
    print()

    # Factor ranges from validation documents
    VALID_RANGES = {
        "fc": (0.55, 0.95),      # Collection feasibility
        "fcp": (0.3, 13.7),      # Competition factor (can be >1)
        "fs": (0.70, 1.0),       # Seasonal concentration
        "fl": (0.65, 1.0),       # Logistics viability
    }

    issues = []
    calculations = []

    for residue_name, data in sorted(SAF_VALIDATION_DATA.items(), key=lambda x: x[1].get("saf_rank", 999)):
        fc = data.get("fc")
        fcp = data.get("fcp")
        fs = data.get("fs")
        fl = data.get("fl")
        saf_real = data.get("saf_real")
        tier = data.get("priority_tier", "UNKNOWN")
        rank = data.get("saf_rank", "?")

        # Calculate what SAF should be
        calculated_saf = calculate_saf_from_factors(fc, fcp, fs, fl)

        # Store for analysis
        calculations.append({
            "name": residue_name,
            "rank": rank,
            "tier": tier,
            "saf_real": saf_real,
            "calculated": calculated_saf,
            "fc": fc,
            "fcp": fcp,
            "fs": fs,
            "fl": fl,
        })

        # Check for issues
        residue_issues = []

        # Check factor ranges
        if fc and not (VALID_RANGES["fc"][0] <= fc <= VALID_RANGES["fc"][1]):
            residue_issues.append(f"FC out of range: {fc} (valid: {VALID_RANGES['fc']})")

        if fcp and not (VALID_RANGES["fcp"][0] <= fcp <= VALID_RANGES["fcp"][1]):
            residue_issues.append(f"FCp out of range: {fcp} (valid: {VALID_RANGES['fcp']})")

        if fs and not (VALID_RANGES["fs"][0] <= fs <= VALID_RANGES["fs"][1]):
            residue_issues.append(f"FS out of range: {fs} (valid: {VALID_RANGES['fs']})")

        if fl and not (VALID_RANGES["fl"][0] <= fl <= VALID_RANGES["fl"][1]):
            residue_issues.append(f"FL out of range: {fl} (valid: {VALID_RANGES['fl']})")

        # Check if calculation matches SAF_REAL (with 5% tolerance for rounding)
        if abs(calculated_saf - saf_real) > 0.5:
            residue_issues.append(f"SAF mismatch: stated={saf_real:.2f}%, calculated={calculated_saf:.2f}%")

        if residue_issues:
            for issue in residue_issues:
                issues.append((rank, residue_name, issue))
                print(f"⚠️  Rank {rank}: {residue_name}")
                print(f"    ❌ {issue}")
                print()

    # Print summary
    print()
    print("=" * 100)
    print("VALIDATION SUMMARY")
    print("=" * 100)
    print()

    if issues:
        print(f"Found {len(issues)} issue(s) requiring attention:\n")
        for rank, name, issue in sorted(issues):
            print(f"  Rank {rank}: {name}")
            print(f"    - {issue}")
        print()
    else:
        print("✅ All SAF calculations are valid!")
        print()

    # Print calculation details for top residues
    print("=" * 100)
    print("TOP 10 RESIDUES - CALCULATION VERIFICATION")
    print("=" * 100)
    print()

    for calc in calculations[:10]:
        match_str = "✅" if abs(calc["calculated"] - calc["saf_real"]) <= 0.5 else "❌"
        print(f"{match_str} Rank {calc['rank']}: {calc['name']:<45} | {calc['tier']:<10}")
        print(f"   SAF:  Stated={calc['saf_real']:.2f}% | Calculated={calc['calculated']:.2f}%")
        print(f"   Factors: FC={calc['fc']:.2f}, FCp={calc['fcp']:.2f}, FS={calc['fs']:.2f}, FL={calc['fl']:.2f}")
        print(f"   Formula: {calc['fc']:.2f} × (1/{calc['fcp']:.2f}) × {calc['fs']:.2f} × {calc['fl']:.2f} = {calc['calculated']:.2f}%")
        print()

    return len(issues) == 0


if __name__ == "__main__":
    success = validate_saf_calculations()
    sys.exit(0 if success else 1)
