
"""
Expand CP2B Database with Complete Excel Data - FIXED VERSION
Automatically finds the Excel file
"""

import sqlite3
import pandas as pd
from pathlib import Path
import shutil
from datetime import datetime
import glob
import os

print("🔧 EXPANDING CP2B DATABASE WITH COMPLETE FIELDS")
print("=" * 80)

# Paths
db_path = "data/cp2b_panorama.db"

# Search for Excel file in multiple locations
excel_patterns = [
    "dossie_final_residuos*.xlsx",
    "*.xlsx",
    "../*.xlsx",
    "../Validacao_dados/**/*.xlsx",
]

excel_file = None
search_dirs = [
    ".",
    "..",
    "../Validacao_dados",
    "../Validacao_dados/05_RESULTADO_FINAL",
]

print("\n🔍 SEARCHING FOR EXCEL FILE:")
print("-" * 80)

for search_dir in search_dirs:
    if not os.path.exists(search_dir):
        continue
        
    print(f"  Searching in: {search_dir}")
    
    for pattern in ["dossie_final_residuos*.xlsx", "*.xlsx"]:
        search_pattern = os.path.join(search_dir, pattern)
        files = glob.glob(search_pattern)
        
        for file in files:
            # Skip temp files
            if '~$' in file or 'temp' in file.lower():
                continue
            
            print(f"    Found: {file}")
            
            # Prefer dossie_final_residuos files
            if 'dossie_final_residuos' in file.lower():
                excel_file = file
                print(f"    ✅ Using: {excel_file}")
                break
        
        if excel_file:
            break
    
    if excel_file:
        break

if not excel_file:
    print("\n❌ ERROR: Excel file not found!")
    print("Please place dossie_final_residuos*.xlsx in the project directory")
    exit(1)

print(f"\n✅ Using Excel file: {excel_file}")
print(f"   Size: {os.path.getsize(excel_file)/1024:.1f} KB")

# Backup database
backup_path = f"data/cp2b_panorama_BACKUP_BEFORE_EXPANSION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
shutil.copy2(db_path, backup_path)
print(f"\n✅ Backup created: {backup_path}")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if columns already exist
cursor.execute("PRAGMA table_info(residuos)")
existing_columns = [col[1] for col in cursor.fetchall()]

if 'generation' in existing_columns:
    print("\n⚠️ New columns already exist - skipping ALTER TABLE")
else:
    print("\n\n📊 STEP 1: ADD NEW COLUMNS TO residuos TABLE")
    print("-" * 80)
    
    new_columns = [
        ("categoria_nome", "TEXT"),
        ("generation", "TEXT"),
        ("destination", "TEXT"),
        ("justification", "TEXT"),
        ("chemical_cn_ratio", "REAL"),
        ("chemical_ch4_content", "REAL"),
        ("bmp_resumo_literatura", "TEXT"),
        ("bmp_referencias_literatura", "TEXT"),
        ("ts_resumo_literatura", "TEXT"),
        ("ts_referencias_literatura", "TEXT"),
        ("vs_resumo_literatura", "TEXT"),
        ("vs_referencias_literatura", "TEXT"),
        ("cn_resumo_literatura", "TEXT"),
        ("cn_referencias_literatura", "TEXT"),
        ("ch4_resumo_literatura", "TEXT"),
        ("ch4_referencias_literatura", "TEXT"),
        ("icon", "TEXT"),
        ("references_count", "INTEGER"),
    ]
    
    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE residuos ADD COLUMN {col_name} {col_type}")
            print(f"  ✅ Added: {col_name:40s} ({col_type})")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"  ⚠️ Exists: {col_name:40s}")
    
    conn.commit()

print("\n\n📊 STEP 2: LOAD DATA FROM EXCEL")
print("-" * 80)

# Read all sheets
xl_file = pd.ExcelFile(excel_file)
all_data = []

for sheet in xl_file.sheet_names:
    print(f"  Reading sheet: {sheet}")
    df = pd.read_excel(excel_file, sheet_name=sheet)
    all_data.append(df)

# Combine all sheets
df_complete = pd.concat(all_data, ignore_index=True)
print(f"\n✅ Total residues in Excel: {len(df_complete)}")

print("\n\n📊 STEP 3: UPDATE DATABASE WITH NEW FIELDS")
print("-" * 80)

updated_count = 0
not_found = []

for idx, row in df_complete.iterrows():
    residuo_codigo = row['Residuo_Codigo']
    
    # Check if residue exists
    cursor.execute("SELECT id FROM residuos WHERE codigo = ?", (residuo_codigo,))
    result = cursor.fetchone()
    
    if not result:
        not_found.append(residuo_codigo)
        continue
    
    # Prepare update data
    update_data = {
        'categoria_nome': row.get('Categoria_Nome'),
        'generation': row.get('generation'),
        'destination': row.get('destination'),
        'justification': row.get('justification'),
        'chemical_cn_ratio': row.get('chemical_cn_ratio'),
        'chemical_ch4_content': row.get('chemical_ch4_content'),
        'bmp_resumo_literatura': row.get('BMP_Resumo_Literatura'),
        'bmp_referencias_literatura': row.get('BMP_Referencias_Literatura'),
        'ts_resumo_literatura': row.get('TS_Resumo_Literatura'),
        'ts_referencias_literatura': row.get('TS_Referencias_Literatura'),
        'vs_resumo_literatura': row.get('VS_Resumo_Literatura'),
        'vs_referencias_literatura': row.get('VS_Referencias_Literatura'),
        'cn_resumo_literatura': row.get('CN_Resumo_Literatura'),
        'cn_referencias_literatura': row.get('CN_Referencias_Literatura'),
        'ch4_resumo_literatura': row.get('CH4_CONTEUDO_Resumo_Literatura'),
        'ch4_referencias_literatura': row.get('CH4_CONTEUDO_Referencias_Literatura'),
        'icon': row.get('icon'),
        'references_count': row.get('references_count'),
    }
    
    # Build UPDATE query
    set_clause = []
    values = []
    
    for field, value in update_data.items():
        if pd.notna(value):
            set_clause.append(f"{field} = ?")
            values.append(value)
    
    if set_clause:
        query = f"UPDATE residuos SET {', '.join(set_clause)} WHERE codigo = ?"
        values.append(residuo_codigo)
        
        cursor.execute(query, values)
        updated_count += 1
        print(f"  ✅ Updated: {row['Residuo_Nome']:40s} ({len(set_clause)} fields)")

conn.commit()

print(f"\n✅ Updated {updated_count}/{len(df_complete)} residues with complete data")

if not_found:
    print(f"\n⚠️ {len(not_found)} residues in Excel not found in database:")
    for codigo in not_found:
        print(f"    - {codigo}")

print("\n\n📊 STEP 4: VERIFY EXPANSION")
print("-" * 80)

# Check a sample record
cursor.execute("""
    SELECT nome, generation, chemical_cn_ratio, bmp_resumo_literatura
    FROM residuos
    WHERE generation IS NOT NULL
    LIMIT 1
""")

row = cursor.fetchone()
if row:
    print("\n✅ Sample verification:")
    print(f"  Nome: {row[0]}")
    print(f"  Generation: {row[1][:80] if row[1] else 'None'}...")
    print(f"  C/N Ratio: {row[2]}")
    print(f"  BMP Literatura: {row[3][:80] if row[3] else 'None'}...")

# Count non-null values for new fields
cursor.execute("SELECT COUNT(*) FROM residuos")
total = cursor.fetchone()[0]

print(f"\n\n📊 DATA COMPLETENESS SUMMARY:")
print("-" * 80)

new_field_names = [
    'categoria_nome', 'generation', 'destination', 'justification',
    'chemical_cn_ratio', 'chemical_ch4_content',
    'bmp_resumo_literatura', 'ts_resumo_literatura', 'vs_resumo_literatura',
    'cn_resumo_literatura', 'ch4_resumo_literatura'
]

for col_name in new_field_names:
    cursor.execute(f"SELECT COUNT(*) FROM residuos WHERE {col_name} IS NOT NULL AND {col_name} != ''")
    non_null = cursor.fetchone()[0]
    percentage = (non_null / total) * 100
    status = "✅" if percentage > 80 else "⚠️" if percentage > 50 else "❌"
    print(f"{status} {col_name:40s}: {non_null:2d}/{total} ({percentage:5.1f}%)")

conn.close()

print("\n\n" + "=" * 80)
print("✅ DATABASE EXPANSION COMPLETE!")
print(f"\n💾 Backup: {backup_path}")
print(f"📊 Database now has {len(existing_columns) + 18} columns")
print("\nNew fields added:")
print("  🔬 C/N Ratio, CH4 Content")
print("  📝 Generation, Destination, Justification")
print("  📚 Literature summaries and references for all parameters")
