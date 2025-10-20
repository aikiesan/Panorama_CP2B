import shutil
from pathlib import Path
import sqlite3
import pandas as pd

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("="*80)
print("MIGRACAO DO BANCO DE DADOS CP2B")
print("="*80)

# Caminhos
project_root = Path(__file__).parent.parent
old_db = project_root / "data" / "cp2b_panorama.db"
new_db = project_root / "webapp" / "panorama_cp2b_final.db"
backup_db = project_root / "data" / "cp2b_panorama_backup.db"

# Verificar existência
if not new_db.exists():
    print(f"❌ Erro: Banco novo não encontrado em {new_db}")
    exit(1)

print(f"\nBanco antigo: {old_db}")
print(f"Banco novo: {new_db}")
print(f"Backup: {backup_db}")

# 1. Backup do banco antigo
print("\n1. Criando backup do banco antigo...")
if old_db.exists():
    shutil.copy2(old_db, backup_db)
    print(f"   OK Backup criado: {backup_db.name}")
else:
    print(f"   AVISO: Banco antigo nao existe, pulando backup")

# 2. Substituir banco
print("\n2. Substituindo banco...")
shutil.copy2(new_db, old_db)
print(f"   OK Banco substituido: {old_db.name}")

# 3. Verificar estrutura
print("\n3. Verificando estrutura do novo banco...")
conn = sqlite3.connect(old_db)

# Listar tabelas
tabelas = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name",
    conn
)

print(f"\nTabelas disponiveis ({len(tabelas)}):")
for _, row in tabelas.iterrows():
    count = pd.read_sql_query(f"SELECT COUNT(*) as c FROM {row['name']}", conn).iloc[0]['c']
    print(f"   OK {row['name']:30s} | {count:>6} registros")

# Verificar colunas críticas da tabela residuos (nova estrutura)
print(f"\nVerificando colunas da tabela 'residuos'...")
colunas = pd.read_sql_query("PRAGMA table_info(residuos)", conn)
colunas_necessarias = ['fc_medio', 'fcp_medio', 'fs_medio', 'fl_medio', 'bmp_medio', 'fator_realista']

for col in colunas_necessarias:
    existe = col in colunas['name'].values
    status = "OK" if existe else "ERRO"
    print(f"   {status} {col}")

conn.close()

print("\n" + "="*80)
print("OK MIGRACAO CONCLUIDA COM SUCESSO!")
print("="*80)
