"""Test POLPA_CITROS update (should have complete data)"""
import sys
sys.path.insert(0, r'C:\Users\Lucas\Documents\CP2B\PanoramaCP2B')

from update_database_from_excel import update_single_residue, RESIDUE_MAPPING

# Test with POLPA_CITROS
code = 'POLPA_CITROS'
if code in RESIDUE_MAPPING:
    sector, filename, var_name = RESIDUE_MAPPING[code]

    print(f"Testing update for {code}")
    print(f"  Sector: {sector}")
    print(f"  File: {filename}")
    print(f"  Variable: {var_name}")
    print()

    success = update_single_residue(code, sector, filename, var_name)
    print(f"\nResult: {'SUCCESS' if success else 'FAILED'}")

    # Show key lines from the generated file
    if success:
        filepath = f'src/data/{sector}/{filename}'
        print(f"\nGenerated file key sections:")
        print("=" * 80)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Show name, generation, BMP, scenarios
            for i, line in enumerate(lines[:60], 1):
                if any(keyword in line for keyword in ['name=', 'generation=', 'bmp=', 'scenarios=', 'Realista']):
                    print(f"{i:3d}: {line.strip()}")
else:
    print(f"{code} not in mapping!")
