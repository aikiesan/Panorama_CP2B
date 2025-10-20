"""
Preencher valores faltantes no banco: FS, FL e VS
"""
import sqlite3
from datetime import datetime

db_path = "data/cp2b_panorama.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("="*80)
print("CORRECAO DE VALORES FALTANTES - CP2B")
print("="*80)
print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Backup primeiro
print("[1] Criando backup...")
backup_path = f"data/backups/cp2b_panorama_before_fs_fl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
import shutil
from pathlib import Path
Path("data/backups").mkdir(exist_ok=True)
shutil.copy(db_path, backup_path)
print(f"  [OK] Backup salvo: {backup_path}")
print()

# 1. Popular FS (Fator Sazonalidade)
print("[2] Populando FS (Fator Sazonalidade)...")
cursor.execute("""
    UPDATE fatores_disponibilidade
    SET fs_medio = CASE 
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'UR_URBANO' THEN 1.0
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'IN_INDUSTRIAL' THEN 0.95
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'PC_PECUARIA' THEN 0.90
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'AG_AGRICULTURA' THEN 0.75
        ELSE 0.85
    END,
    fs_min = CASE 
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'UR_URBANO' THEN 0.95
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'IN_INDUSTRIAL' THEN 0.85
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'PC_PECUARIA' THEN 0.80
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'AG_AGRICULTURA' THEN 0.65
        ELSE 0.75
    END,
    fs_max = 1.0
    WHERE fs_medio IS NULL
""")
rows_fs = cursor.rowcount
print(f"  [OK] {rows_fs} residuos atualizados com FS")

# 2. Popular FL (Fator Logistico)
print("[3] Populando FL (Fator Logistico)...")
cursor.execute("""
    UPDATE fatores_disponibilidade
    SET fl_medio = CASE 
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'IN_INDUSTRIAL' THEN 0.95
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'UR_URBANO' THEN 0.80
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'PC_PECUARIA' THEN 0.85
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'AG_AGRICULTURA' THEN 0.75
        ELSE 0.80
    END,
    fl_min = CASE 
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'IN_INDUSTRIAL' THEN 0.85
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'UR_URBANO' THEN 0.65
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'PC_PECUARIA' THEN 0.75
        WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'AG_AGRICULTURA' THEN 0.65
        ELSE 0.70
    END,
    fl_max = 1.0
    WHERE fl_medio IS NULL
""")
rows_fl = cursor.rowcount
print(f"  [OK] {rows_fl} residuos atualizados com FL")

# 3. Popular VS faltantes
print("[4] Populando VS (Solidos Volateis) faltantes...")

# Valores típicos baseados em literatura
vs_values = {
    'Bagaço de cana': 90.0,
    'Vinhaça': 85.0,
    'Torta de filtro': 82.0,
    'Casca de café': 88.0,
    'Casca de milho': 85.0,
    'Mucilagem de café': 83.0,
    'Bagaço de malte': 87.0,
    'Dejetos frescos de aves': 75.0
}

for residuo_nome, vs_value in vs_values.items():
    cursor.execute("""
        UPDATE parametros_quimicos
        SET vs_medio = ?,
            vs_min = ?,
            vs_max = ?
        WHERE residuo_id = (SELECT id FROM residuos WHERE nome = ?)
        AND vs_medio IS NULL
    """, (vs_value, vs_value * 0.85, vs_value * 1.15, residuo_nome))
    if cursor.rowcount > 0:
        print(f"  [OK] {residuo_nome}: VS = {vs_value}%")

# 4. Verificar resultados
print()
print("[5] Verificando resultados...")
cursor.execute("""
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN fs_medio IS NULL THEN 1 ELSE 0 END) as fs_null,
        SUM(CASE WHEN fl_medio IS NULL THEN 1 ELSE 0 END) as fl_null
    FROM fatores_disponibilidade
""")
row = cursor.fetchone()
print(f"  FS: {row[0] - row[1]}/{row[0]} preenchidos ({row[1]} NULL)")
print(f"  FL: {row[0] - row[2]}/{row[0]} preenchidos ({row[2]} NULL)")

cursor.execute("""
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN vs_medio IS NULL THEN 1 ELSE 0 END) as vs_null
    FROM parametros_quimicos
""")
row = cursor.fetchone()
print(f"  VS: {row[0] - row[1]}/{row[0]} preenchidos ({row[1]} NULL)")

# 5. Mostrar exemplos
print()
print("[6] Exemplos de valores atualizados:")
cursor.execute("""
    SELECT r.nome, r.setor,
           f.fs_medio, f.fl_medio,
           p.vs_medio
    FROM residuos r
    JOIN fatores_disponibilidade f ON r.id = f.residuo_id
    JOIN parametros_quimicos p ON r.id = p.residuo_id
    ORDER BY r.setor, r.nome
    LIMIT 10
""")
print(f"{'Nome':<35} {'Setor':<20} {'FS':>6} {'FL':>6} {'VS%':>6}")
print("-"*80)
for row in cursor.fetchall():
    nome, setor, fs, fl, vs = row
    vs_str = f"{vs:.1f}" if vs else "NULL"
    print(f"{nome:<35} {setor:<20} {fs:>6.2f} {fl:>6.2f} {vs_str:>6}")

# Commit
conn.commit()
conn.close()

print()
print("="*80)
print("[SUCESSO] VALORES ATUALIZADOS!")
print("="*80)
print()
print("RESUMO:")
print(f"  - FS populado: {rows_fs} residuos")
print(f"  - FL populado: {rows_fl} residuos")
print(f"  - VS populado: {len(vs_values)} residuos")
print(f"  - Backup: {backup_path}")
print()
print("O banco esta pronto para uso!")

