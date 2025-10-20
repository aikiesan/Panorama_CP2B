import pandas as pd
import sys

# Read the Excel file
file_path = r'C:\Users\Lucas\Documents\CP2B\Validacao_dados\dossie_final_residuos_20251020_112818_v9_CITROS_VALIDADO.xlsx'
df = pd.read_excel(file_path, sheet_name='AG_AGRICULTURA')

# Display basic info
print("=" * 80)
print("VALIDATED EXCEL FILE INSPECTION")
print("=" * 80)
print(f"\nTotal rows: {len(df)}")
print(f"\nColumns ({len(df.columns)}):")
for col in df.columns:
    print(f"  - {col}")

# Check for a well-populated row
print("\n" + "=" * 80)
print("SAMPLE VALIDATED ROW (POLPA_CITROS)")
print("=" * 80)
citros_rows = df[df['Residuo_Codigo'] == 'POLPA_CITROS']
if len(citros_rows) > 0:
    row = citros_rows.iloc[0]
    key_fields = [
        'Residuo_Codigo', 'Residuo_Nome', 'generation', 'destination',
        'chemical_bmp', 'chemical_ts', 'chemical_vs', 'chemical_cn_ratio',
        'availability_fc', 'availability_fcp', 'availability_final_availability',
        'BMP_Resumo_Literatura', 'BMP_Referencias_Literatura'
    ]
    for field in key_fields:
        if field in row:
            val = row[field]
            if pd.notna(val):
                print(f"\n{field}:")
                val_str = str(val)
                if len(val_str) > 200:
                    print(f"  {val_str[:200]}...")
                else:
                    print(f"  {val_str}")
            else:
                print(f"\n{field}: <empty>")
else:
    print("POLPA_CITROS not found!")

# Check another row
print("\n" + "=" * 80)
print("SAMPLE ROW 2 (BAGACO)")
print("=" * 80)
bagaco_rows = df[df['Residuo_Codigo'] == 'BAGACO']
if len(bagaco_rows) > 0:
    row = bagaco_rows.iloc[0]
    for field in ['Residuo_Nome', 'BMP_Resumo_Literatura', 'TS_Resumo_Literatura']:
        if field in row:
            val = row[field]
            print(f"\n{field}: {val if pd.notna(val) else '<empty>'}")
