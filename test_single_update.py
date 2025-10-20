"""Test single residue update"""
import sys
sys.path.insert(0, r'C:\Users\Lucas\Documents\CP2B\PanoramaCP2B')

from update_database_from_excel import update_single_residue, RESIDUE_MAPPING

# Test with BAGACO first
code = 'BAGACO'
sector, filename, var_name = RESIDUE_MAPPING[code]

print(f"Testing update for {code}")
print(f"  Sector: {sector}")
print(f"  File: {filename}")
print(f"  Variable: {var_name}")
print()

success = update_single_residue(code, sector, filename, var_name)
print(f"\nResult: {'SUCCESS' if success else 'FAILED'}")

# Show the generated file
if success:
    filepath = f'src/data/{sector}/{filename}'
    print(f"\nGenerated file preview (first 50 lines):")
    print("=" * 80)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()[:50]
        for i, line in enumerate(lines, 1):
            print(f"{i:3d}: {line}", end='')
