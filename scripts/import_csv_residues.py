"""
CSV Residue Import Script
Parses CSV data and generates residue data files

Usage:
    python scripts/import_csv_residues.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.csv_importer import parse_csv_to_residues, generate_residue_file


def main():
    """Main import function"""
    # CSV file path
    csv_path = project_root / "Planilha de Organização de Dados - Projeto CP2B.xlsx - Resíduo_Disponível (1).csv"

    if not csv_path.exists():
        print(f"[ERROR] CSV file not found: {csv_path}")
        return

    print(f"[INFO] Reading CSV: {csv_path.name}")
    print("=" * 80)

    # Parse CSV
    try:
        residues = parse_csv_to_residues(str(csv_path))
        print(f"[SUCCESS] Parsed {len(residues)} residues from CSV\n")
    except Exception as e:
        print(f"[ERROR] Error parsing CSV: {e}")
        import traceback
        traceback.print_exc()
        return

    # Group by category
    by_category = {}
    for residue in residues:
        category = residue['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(residue)

    print("[INFO] Residues by Category:")
    for category, items in by_category.items():
        print(f"  {category}: {len(items)} residues")
    print()

    # Generate files
    print("[INFO] Generating Python data files...")
    print("=" * 80)

    generated_files = []

    for category, items in by_category.items():
        # Map category to directory
        category_map = {
            "Agricultura": "agricultura",
            "Pecuária": "pecuaria",
            "Urbano": "urbano",
            "Industrial": "industrial"
        }

        dir_name = category_map.get(category, category.lower())
        output_dir = project_root / "src" / "data" / dir_name

        print(f"\n[CATEGORY] {category} -> {output_dir}")

        for residue in items:
            try:
                filepath = generate_residue_file(residue, output_dir)
                generated_files.append(filepath)
                print(f"  [OK] Generated: {Path(filepath).name}")
            except Exception as e:
                print(f"  [ERROR] Error generating {residue['name']}: {e}")

    print("\n" + "=" * 80)
    print(f"[SUCCESS] Successfully generated {len(generated_files)} files")
    print("\n[IMPORTANT] Remember to:")
    print("  1. Review generated files for TODO items")
    print("  2. Add actual availability factors (FC, FCp, FS, FL)")
    print("  3. Calculate scenario potentials (Pessimista, Realista, Otimista, Teorico)")
    print("  4. Parse and add scientific references")
    print("  5. Update sector __init__.py files to import new residues")
    print("  6. Add TS and VS values from data sources")


if __name__ == "__main__":
    main()
