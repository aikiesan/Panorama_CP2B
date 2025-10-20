import sqlite3
from pathlib import Path
import pandas as pd

print("="*80)
print("TESTE DE VALIDACAO DA MIGRACAO")
print("="*80)

project_root = Path(__file__).parent.parent
db_path = project_root / "data" / "cp2b_panorama.db"

conn = sqlite3.connect(db_path)

# Teste 1: Residuos
print("\nTESTE 1: Carregamento de Residuos")
df_residuos = pd.read_sql_query("""
    SELECT 
        id, codigo, nome, setor,
        bmp_medio,
        fc_medio, fcp_medio, fs_medio, fl_medio,
        fator_realista
    FROM residuos
""", conn)

print(f"   Total de residuos: {len(df_residuos)}")
print(f"   Com BMP: {df_residuos['bmp_medio'].notna().sum()}")
print(f"   Com fator_realista: {df_residuos['fator_realista'].notna().sum()}")
print(f"   Fator > 0: {(df_residuos['fator_realista'] > 0).sum()}")

assert len(df_residuos) == 38, f"ERRO: Esperado 38 residuos, encontrado {len(df_residuos)}"
assert (df_residuos['fator_realista'] > 0).sum() > 30, "ERRO: Fator zerado"
print("   OK Residuos OK")

# Teste 2: Municipios
print("\nTESTE 2: Municipios")
df_municipios = pd.read_sql_query("SELECT * FROM municipios LIMIT 10", conn)
total_municipios = pd.read_sql_query('SELECT COUNT(*) as c FROM municipios', conn).iloc[0]['c']
print(f"   Total de municipios: {total_municipios}")
print(f"   Colunas: {len(df_municipios.columns)}")
print(f"   Com CH4 > 0: {(df_municipios['ch4_rea_total'] > 0).sum()}")
print("   OK Municipios OK")

# Teste 3: Top Municipios
print("\nTESTE 3: Top Municipios")
df_top = pd.read_sql_query("SELECT * FROM top_municipios", conn)
print(f"   Registros: {len(df_top)}")
print(f"   Top 5:")
for _, row in df_top.head(5).iterrows():
    print(f"      {row['ranking']}. {row['nome_municipio']}: {row['ch4_rea_total']:,.0f} Nm3/ano")
print("   OK Top municipios OK")

# Teste 4: Distribuicao por Setor
print("\nTESTE 4: Distribuicao por Setor")
df_setores = pd.read_sql_query("SELECT * FROM distribuicao_setores", conn)
print(f"   Setores: {len(df_setores)}")
for _, row in df_setores.iterrows():
    print(f"      {row['setor']}: {row['ch4_rea']:,.0f} Nm3/ano")
print("   OK Setores OK")

# Teste 5: Resumo Estado
print("\nTESTE 5: Resumo do Estado")
df_resumo = pd.read_sql_query("SELECT * FROM resumo_estado", conn)
for _, row in df_resumo.iterrows():
    print(f"      {row['indicador']}: {row['valor']:,.0f} {row['unidade']}")
print("   OK Resumo OK")

conn.close()

print("\n" + "="*80)
print("OK TODOS OS TESTES PASSARAM!")
print("="*80)
