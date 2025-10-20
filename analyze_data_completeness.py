import pandas as pd

df = pd.read_excel(r'C:\Users\Lucas\Documents\CP2B\Validacao_dados\dossie_final_residuos_20251020_112818_v9_CITROS_VALIDADO.xlsx', sheet_name='AG_AGRICULTURA')

# Key fields that indicate "complete" data
key_fields = ['generation', 'destination', 'chemical_bmp', 'chemical_ts', 'chemical_vs', 'availability_fc']

print("Data Completeness Analysis")
print("=" * 80)
print(f"{'Residuo_Codigo':<20} {'Cultura':<20} {'Complete Fields':<15} {'Status'}")
print("-" * 80)

for _, row in df.iterrows():
    code = row['Residuo_Codigo']
    cultura = row.get('Categoria_Nome', 'Unknown')
    complete_count = sum(1 for field in key_fields if pd.notna(row[field]) and row[field] != '')
    status = "GOOD" if complete_count >= 4 else "PARTIAL" if complete_count >= 2 else "MINIMAL"

    print(f"{code:<20} {str(cultura):<20} {complete_count}/{len(key_fields)}             {status}")

print("\nSummary by Culture:")
print("=" * 80)
cultures = df.groupby('Categoria_Nome')
for cultura, group in cultures:
    avg_complete = sum(sum(1 for field in key_fields if pd.notna(row[field]))  for _, row in group.iterrows()) / (len(group) * len(key_fields))
    print(f"{cultura}: {len(group)} residues, {avg_complete*100:.1f}% average completeness")
