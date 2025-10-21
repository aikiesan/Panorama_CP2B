
"""
Complete Database Schema and Content Inspector
CP2B Project - Check all fields and data structure
"""

import sqlite3
import pandas as pd

print("🔍 CP2B DATABASE COMPLETE INSPECTION")
print("=" * 80)

db_path = "data/cp2b_panorama.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ============================================================================
# STEP 1: LIST ALL TABLES
# ============================================================================
print("\n📋 STEP 1: ALL TABLES")
print("-" * 80)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [t[0] for t in cursor.fetchall()]

for i, table in enumerate(tables, 1):
    print(f"  {i}. {table}")

# ============================================================================
# STEP 2: DETAILED SCHEMA FOR residuos TABLE
# ============================================================================
print("\n\n📊 STEP 2: SCHEMA FOR 'residuos' TABLE")
print("=" * 80)

cursor.execute("PRAGMA table_info(residuos)")
columns = cursor.fetchall()

print(f"\nTotal columns: {len(columns)}\n")

# Categorize columns
basic_cols = []
chemical_cols = []
availability_cols = []
reference_cols = []

for col in columns:
    col_id, col_name, col_type, not_null, default, pk = col
    
    if any(x in col_name.lower() for x in ['bmp', 'ts', 'vs', 'cod', 'dqo', 'ph', 'alcal', 'nitrog', 'cnpks']):
        chemical_cols.append(col_name)
    elif any(x in col_name.lower() for x in ['fc', 'fcp', 'fs', 'fl', 'fator', 'saf']):
        availability_cols.append(col_name)
    elif any(x in col_name.lower() for x in ['ref', 'doi', 'fonte']):
        reference_cols.append(col_name)
    else:
        basic_cols.append(col_name)

print("📝 BASIC INFO FIELDS ({} columns):".format(len(basic_cols)))
for col in basic_cols:
    print(f"  - {col}")

print(f"\n🔬 CHEMICAL PARAMETER FIELDS ({len(chemical_cols)} columns):")
for col in chemical_cols:
    print(f"  - {col}")

print(f"\n📊 AVAILABILITY FACTOR FIELDS ({len(availability_cols)} columns):")
for col in availability_cols:
    print(f"  - {col}")

print(f"\n📚 REFERENCE FIELDS ({len(reference_cols)} columns):")
for col in reference_cols:
    print(f"  - {col}")

# ============================================================================
# STEP 3: SAMPLE DATA - COMPLETE RECORD
# ============================================================================
print("\n\n📊 STEP 3: COMPLETE RECORD FOR 'Bagaço de cana'")
print("=" * 80)

cursor.execute("SELECT * FROM residuos WHERE nome = ?", ("Bagaço de cana",))
row = cursor.fetchone()

if row:
    cursor.execute("PRAGMA table_info(residuos)")
    columns = cursor.fetchall()
    
    print("\n🔬 CHEMICAL PARAMETERS:")
    print("-" * 60)
    for i, col in enumerate(columns):
        col_name = col[1]
        if col_name in chemical_cols:
            value = row[i]
            print(f"  {col_name:30s}: {value}")
    
    print("\n📊 AVAILABILITY FACTORS:")
    print("-" * 60)
    for i, col in enumerate(columns):
        col_name = col[1]
        if col_name in availability_cols:
            value = row[i]
            if 'fator' in col_name.lower() and value is not None:
                print(f"  {col_name:30s}: {value:.4f} ({value*100:.2f}%)")
            else:
                print(f"  {col_name:30s}: {value}")
    
    print("\n📝 BASIC INFO:")
    print("-" * 60)
    for i, col in enumerate(columns):
        col_name = col[1]
        if col_name in basic_cols:
            value = row[i]
            print(f"  {col_name:30s}: {value}")
else:
    print("❌ Not found!")

# ============================================================================
# STEP 4: CHECK NULL VALUES IN CHEMICAL PARAMETERS
# ============================================================================
print("\n\n📊 STEP 4: NULL/MISSING VALUES IN CHEMICAL PARAMETERS")
print("=" * 80)

cursor.execute(f"SELECT COUNT(*) FROM residuos")
total_residues = cursor.fetchone()[0]

print(f"\nTotal residues: {total_residues}\n")

for col_name in chemical_cols:
    cursor.execute(f"SELECT COUNT(*) FROM residuos WHERE {col_name} IS NOT NULL AND {col_name} != 0")
    non_null_count = cursor.fetchone()[0]
    
    percentage = (non_null_count / total_residues) * 100
    status = "✅" if percentage > 80 else "⚠️" if percentage > 50 else "❌"
    
    print(f"{status} {col_name:30s}: {non_null_count:2d}/{total_residues} ({percentage:5.1f}%)")

# ============================================================================
# STEP 5: CHECK WHAT get_residue_by_name() RETURNS
# ============================================================================
print("\n\n📊 STEP 5: TEST get_residue_by_name() FUNCTION")
print("=" * 80)

from src.data_handler import get_residue_by_name

test_residues = ['Bagaço de cana', 'Palha de cana', 'Lodo primário']

for residue_name in test_residues:
    print(f"\n🧪 Testing: {residue_name}")
    print("-" * 60)
    
    result = get_residue_by_name(residue_name)
    
    if result:
        if isinstance(result, dict):
            print(f"  ✅ Returns dict with {len(result)} keys")
            
            # Check for chemical parameters
            chem_keys = [k for k in result.keys() if any(x in k.lower() for x in ['bmp', 'ts', 'vs'])]
            print(f"  🔬 Chemical params in result: {len(chem_keys)}")
            if chem_keys:
                for key in chem_keys[:5]:
                    print(f"      - {key}: {result[key]}")
            else:
                print(f"      ⚠️ NO chemical parameters found in result!")
            
            # Check for availability factors
            avail_keys = [k for k in result.keys() if any(x in k.lower() for x in ['fator', 'fc', 'fs'])]
            print(f"  📊 Availability factors in result: {len(avail_keys)}")
            if avail_keys:
                for key in avail_keys[:5]:
                    print(f"      - {key}: {result[key]}")
        else:
            print(f"  ⚠️ Returns: {type(result)}")
    else:
        print(f"  ❌ Returns None!")

conn.close()

print("\n\n" + "=" * 80)
print("✅ INSPECTION COMPLETE!")
print("\nNow you know:")
print("  1. What fields exist in the database")
print("  2. What data is actually stored")
print("  3. What get_residue_by_name() returns")
print("  4. If chemical parameters are being loaded")
