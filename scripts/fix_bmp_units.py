"""
Fix BMP Range Units - Convert from mL/g to m³/kg

Converts BMP ranges in all residue files from mL CH₄/g VS to m³ CH₄/kg VS
Conversion factor: 1 mL/g = 0.001 m³/kg (divide by 1000)
"""

import re
from pathlib import Path

def convert_bmp_range_units(file_path: Path) -> bool:
    """
    Convert BMP range from mL/g to m³/kg in a residue file.

    Args:
        file_path: Path to residue Python file

    Returns:
        bool: True if file was modified
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    modified = False

    # Pattern to find BMP ranges with mL/g units
    # Example: bmp_range=ParameterRange(min=80.0, mean=115.0, max=150.0, unit="mL CH₄/g VS")
    pattern = r'bmp_range=ParameterRange\(\s*min=([\d.]+),\s*mean=([\d.]+),\s*max=([\d.]+),\s*unit="mL CH₄/g VS"\s*\)'

    def convert_match(match):
        nonlocal modified
        min_val = float(match.group(1))
        mean_val = float(match.group(2))
        max_val = float(match.group(3))

        # Convert from mL/g to m³/kg (divide by 1000)
        new_min = min_val / 1000
        new_mean = mean_val / 1000
        new_max = max_val / 1000

        modified = True
        return f'bmp_range=ParameterRange(min={new_min}, mean={new_mean}, max={new_max}, unit="m³ CH₄/kg VS")'

    content = re.sub(pattern, convert_match, content)

    # Also handle alternative unit formats
    pattern2 = r'bmp_range=ParameterRange\(\s*min=([\d.]+),\s*mean=([\d.]+),\s*max=([\d.]+),\s*unit="mL/g"\s*\)'

    def convert_match2(match):
        nonlocal modified
        min_val = float(match.group(1))
        mean_val = float(match.group(2))
        max_val = float(match.group(3))

        new_min = min_val / 1000
        new_mean = mean_val / 1000
        new_max = max_val / 1000

        modified = True
        return f'bmp_range=ParameterRange(min={new_min}, mean={new_mean}, max={new_max}, unit="m³/kg")'

    content = re.sub(pattern2, convert_match2, content)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Converted: {file_path.name}")
        return True

    return False


def main():
    """Convert BMP ranges for all residue files."""
    project_root = Path(__file__).parent.parent

    sectors = ['agricultura', 'pecuaria', 'urbano', 'industrial']
    total_converted = 0
    total_files = 0

    for sector in sectors:
        sector_path = project_root / 'src' / 'data' / sector
        if not sector_path.exists():
            continue

        print(f"\n{'='*60}")
        print(f"Processing {sector.upper()} sector...")
        print(f"{'='*60}")

        # Get all Python files except __init__.py
        residue_files = [f for f in sector_path.glob('*.py') if f.name != '__init__.py']

        for file_path in residue_files:
            total_files += 1
            if convert_bmp_range_units(file_path):
                total_converted += 1

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total files processed: {total_files}")
    print(f"Files converted: {total_converted}")
    print(f"Files unchanged: {total_files - total_converted}")
    print(f"\nConversion complete! BMP ranges now in m³/kg units.")


if __name__ == '__main__':
    main()
