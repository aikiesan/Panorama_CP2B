import pandas as pd
import sys
import re
sys.path.insert(0, r'C:\Users\Lucas\Documents\CP2B\PanoramaCP2B')
from update_database_from_excel import parse_reference_string, parse_all_references

df = pd.read_excel(r'C:\Users\Lucas\Documents\CP2B\Validacao_dados\dossie_final_residuos_20251020_112818_v9_CITROS_VALIDADO.xlsx', sheet_name='AG_AGRICULTURA')

# Test with TS reference from BAGACO
print("=" * 80)
print("Test 1: BAGACO TS Reference")
print("=" * 80)
row = df[df['Residuo_Codigo'] == 'BAGACO'].iloc[0]
ref_str = row['TS_Referencias_Literatura']
if pd.notna(ref_str):
    print(f"\nRaw string:\n{ref_str}\n")
    parsed = parse_reference_string(ref_str)
    if parsed:
        print("Parsed result:")
        for key, val in parsed.items():
            if key != 'key_findings':
                print(f"  {key}: {val}")

# Test with POLPA_CITROS
print("\n" + "=" * 80)
print("Test 2: POLPA_CITROS All References")
print("=" * 80)
row2 = df[df['Residuo_Codigo'] == 'POLPA_CITROS'].iloc[0]
all_refs = parse_all_references(row2)
print(f"\nTotal references parsed: {len(all_refs)}")
if all_refs:
    print("\nFirst 2 references:")
    for i, ref in enumerate(all_refs[:2], 1):
        print(f"\n  Reference {i}:")
        print(f"    Authors: {ref['authors'][:80]}...")
        print(f"    Title: {ref['title'][:80]}...")
        print(f"    Journal: {ref['journal']}")
        print(f"    Year: {ref['year']}")
        print(f"    DOI: {ref['doi']}")
