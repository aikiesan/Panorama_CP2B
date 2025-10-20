import pandas as pd

df = pd.read_excel(r'C:\Users\Lucas\Documents\CP2B\Validacao_dados\dossie_final_residuos_20251020_112818_v9_CITROS_VALIDADO.xlsx', sheet_name='AG_AGRICULTURA')
row = df[df['Residuo_Codigo'] == 'BAGACO'].iloc[0]

fields_to_check = [
    'Residuo_Nome', 'generation', 'destination', 'icon', 'justification',
    'chemical_bmp', 'chemical_ts', 'chemical_vs', 'chemical_cn_ratio',
    'availability_fc', 'availability_fcp', 'availability_final_availability',
    'scenarios_realista', 'BMP_Resumo_Literatura', 'TS_Resumo_Literatura'
]

print("BAGACO Excel Data:")
print("=" * 80)
for field in fields_to_check:
    val = row[field]
    print(f"{field:40s}: {val if pd.notna(val) else '<EMPTY>'}")
