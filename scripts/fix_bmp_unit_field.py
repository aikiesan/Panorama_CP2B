"""
Fix BMP Unit Field - Convert bmp_unit from mL to m³

Converts bmp_unit fields in all residue files from "mL CH₄/g VS" to "m³ CH₄/kg VS"
"""

import re
from pathlib import Path

def fix_bmp_unit_field(file_path: Path) -> bool:
    """
    Convert bmp_unit field from mL to m³ in a residue file.

    Args:
        file_path: Path to residue Python file

    Returns:
        bool: True if file was modified
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Replace bmp_unit field
    content = content.replace('bmp_unit="mL CH₄/g VS"', 'bmp_unit="m³ CH₄/kg VS"')
    content = content.replace("bmp_unit='mL CH₄/g VS'", "bmp_unit='m³ CH₄/kg VS'")

    # Also handle variations
    content = content.replace('bmp_unit="mL/g"', 'bmp_unit="m³/kg"')
    content = content.replace("bmp_unit='mL/g'", "bmp_unit='m³/kg'")

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Fixed: {file_path.name}")
        return True

    return False


def main():
    """Fix bmp_unit for all residue files."""
    project_root = Path(__file__).parent.parent

    sectors = ['agricultura', 'pecuaria', 'urbano', 'industrial']
    total_fixed = 0
    total_files = 0

    for sector in sectors:
        sector_path = project_root / 'src' / 'data' / sector
        if not sector_path.exists():
            continue

        print(f"\nProcessing {sector.upper()} sector...")

        # Get all Python files except __init__.py
        residue_files = [f for f in sector_path.glob('*.py') if f.name != '__init__.py']

        for file_path in residue_files:
            total_files += 1
            if fix_bmp_unit_field(file_path):
                total_fixed += 1

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total files processed: {total_files}")
    print(f"Files fixed: {total_fixed}")
    print(f"Files unchanged: {total_files - total_fixed}")
    print(f"\nBMP unit field conversion complete!")


if __name__ == '__main__':
    main()
