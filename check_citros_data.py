import pandas as pd

df = pd.read_excel(r'C:\Users\Lucas\Documents\CP2B\Validacao_dados\dossie_final_residuos_20251020_112818_v9_CITROS_VALIDADO.xlsx', sheet_name='AG_AGRICULTURA')
row = df[df['Residuo_Codigo'] == 'POLPA_CITROS'].iloc[0]

fields_to_check = [
    'Residuo_Nome', 'generation', 'destination', 'icon', 'justification',
    'chemical_bmp', 'chemical_ts', 'chemical_vs', 'chemical_cn_ratio', 'chemical_ch4_content',
    'availability_fc', 'availability_fcp', 'availability_final_availability',
    'scenarios_pessimista', 'scenarios_realista', 'scenarios_otimista',
    'BMP_Resumo_Literatura', 'TS_Resumo_Literatura', 'CN_Resumo_Literatura'
]

print("POLPA_CITROS Excel Data (Validated Citros residue):")
print("=" * 80)
for field in fields_to_check:
    val = row[field]
    if pd.notna(val):
        val_str = str(val)
        if len(val_str) > 60:
            val_str = val_str[:60] + '...'
        print(f"{field:45s}: {val_str}")
    else:
        print(f"{field:45s}: <EMPTY>")
