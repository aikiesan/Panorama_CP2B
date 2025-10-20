#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Persist SAF Data to Residue Files - Phase 5
Writes SAF validation data to the actual source files (destructive operation!)
Usage: python scripts/persist_saf_to_files.py
"""

import sys
import io
import re
from pathlib import Path

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.phase_5_saf_data import SAF_VALIDATION_DATA
from src.data.residue_registry import RESIDUES_REGISTRY, RESIDUE_FILE_MAPPING

def get_residue_file_path(residue_name):
    """Get the file path for a residue"""
    # Check if there's an explicit mapping
    if hasattr(RESIDUE_FILE_MAPPING, '__contains__') and residue_name in RESIDUE_FILE_MAPPING:
        return RESIDUE_FILE_MAPPING[residue_name]

    # Try to find it dynamically
    for sector_dir in [project_root / "src/data/agricultura",
                       project_root / "src/data/pecuaria",
                       project_root / "src/data/urbano",
                       project_root / "src/data/industrial"]:
        if sector_dir.exists():
            for py_file in sector_dir.glob("*.py"):
                if py_file.name == "__init__.py":
                    continue
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Look for the residue name in the file
                        if residue_name in content or residue_name.upper() in content:
                            return py_file
                except:
                    continue

    return None

def add_saf_fields_to_file(file_path, saf_data):
    """Add SAF fields to a residue file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if SAF fields already exist
    if 'Phase 5: SAF Validation Fields' in content:
        print(f"[SKIP] {file_path.name:<40} | SAF fields already present")
        return False

    # Find the closing parenthesis of the ResidueData constructor
    # We need to add SAF fields before the final closing parenthesis
    match = re.search(r'(references=\[\][,\s]*)\)', content)

    if not match:
        print(f"[ERR] {file_path.name:<40} | Could not find insertion point")
        return False

    # Build SAF fields string
    saf_fields = f"""

    # Phase 5: SAF Validation Fields
    saf_real={saf_data.get('saf_real')},
    priority_tier="{saf_data.get('priority_tier')}",
    recommendation="{saf_data.get('recommendation')}",
    saf_rank={saf_data.get('saf_rank')},
    fc_value={saf_data.get('fc')},
    fcp_value={saf_data.get('fcp')},
    fs_value={saf_data.get('fs')},
    fl_value={saf_data.get('fl')},
    culture_group="{saf_data.get('culture_group', 'Unknown')}"
"""

    # Insert SAF fields before the closing parenthesis
    new_content = content[:match.end(1)] + saf_fields + content[match.end(1):]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] {file_path.name:<40} | SAF: {saf_data.get('saf_real'):.2f}% | {saf_data.get('priority_tier')}")
    return True

def persist_saf_to_files():
    """Apply SAF data to all residue files"""
    applied = 0
    skipped = 0
    errors = 0

    print("=" * 80)
    print("PHASE 5: Persisting SAF Data to Residue Files (Destructive)")
    print("=" * 80)
    print()

    for residue_name, saf_data in SAF_VALIDATION_DATA.items():
        file_path = get_residue_file_path(residue_name)

        if not file_path or not file_path.exists():
            print(f"[WARN] {residue_name:<40} | File not found")
            skipped += 1
            continue

        try:
            if add_saf_fields_to_file(file_path, saf_data):
                applied += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"[ERR] {residue_name:<40} | {str(e)}")
            errors += 1

    print()
    print("=" * 80)
    print(f"RESULTS:")
    print(f"  [OK] Applied to:   {applied} residue files")
    print(f"  [SKIP] Skipped:    {skipped} residues")
    print(f"  [ERR] Errors:      {errors} residues")
    print(f"  Total SAF data:    {applied + skipped + errors}")
    print("=" * 80)
    print()

    return applied, skipped, errors

if __name__ == "__main__":
    print("[WARNING] This script modifies residue source files!")
    print("[WARNING] Make sure you have a backup of src/data/ directory")
    print()

    response = input("Continue? (yes/no): ").strip().lower()
    if response != "yes":
        print("Cancelled.")
        sys.exit(0)

    print()
    applied, skipped, errors = persist_saf_to_files()

    if applied > 0:
        print()
        print(f"SUCCESS: Persisted SAF to {applied} residue files")
        print(f"Next: Run 'git diff' to review changes before committing")
    else:
        print()
        print("No changes made")
