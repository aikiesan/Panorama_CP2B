import pandas as pd

df = pd.read_excel(r'C:\Users\Lucas\Documents\CP2B\Validacao_dados\dossie_final_residuos_20251020_112818_v9_CITROS_VALIDADO.xlsx', sheet_name='AG_AGRICULTURA')

for code in ['CASCA_EUCALIPTO', 'GALHOS_EUCALIPTO']:
    print(f'\n=== {code} ===')
    row = df[df['Residuo_Codigo'] == code].iloc[0]
    fields = ['Residuo_Nome', 'generation', 'destination', 'chemical_bmp', 'chemical_ts', 'chemical_vs', 'chemical_cn_ratio', 'chemical_ch4_content', 'availability_fc', 'availability_fcp', 'availability_final_availability', 'scenarios_realista', 'justification']
    for f in fields:
        if pd.notna(row[f]):
            print(f'{f}: {row[f]}')
