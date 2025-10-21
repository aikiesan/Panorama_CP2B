
"""
Inspect the complete 660 KB database to see what data it has
that we can merge into current database
"""

import sqlite3
import pandas as pd

print("🔍 INSPECTING COMPLETE DATABASE")
print("=" * 80)

# Paths
old_db_path = r"C:\Users\Lucas\Documents\CP2B\Validacao_dados\08_DOCUMENTACAO\Backups\cp2b_panorama.db"
current_db_path = r"C:\Users\Lucas\Documents\CP2B\PanoramaCP2B\data\cp2b_panorama.db"

# Connect to old database
print("\n📊 OLD DATABASE (660 KB):")
print("-" * 80)

conn_old = sqlite3.connect(old_db_path)
cursor_old = conn_old.cursor()

# Get all tables
cursor_old.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables_old = cursor_old.fetchall()

print(f"\nTables: {len(tables_old)}")
for table in tables_old:
    print(f"  - {table[0]}")

# Check residuos table structure
cursor_old.execute("PRAGMA table_info(residuos)")
columns_old = cursor_old.fetchall()

print(f"\n\n📋 RESIDUOS TABLE IN OLD DB:")
print(f"   Columns: {len(columns_old)}")
print("-" * 80)

for col in columns_old:
    col_id, col_name, col_type, not_null, default, pk = col
    print(f"  {col_id:2d}. {col_name:35s} {col_type:15s}")

# Count rows
cursor_old.execute("SELECT COUNT(*) FROM residuos")
count_old = cursor_old.fetchone()[0]
print(f"\n   Rows: {count_old}")

# Sample data
print("\n\n📊 SAMPLE DATA (First residue):")
print("-" * 80)

cursor_old.execute("SELECT * FROM residuos LIMIT 1")
row = cursor_old.fetchone()

cursor_old.execute("PRAGMA table_info(residuos)")
columns = cursor_old.fetchall()

if row:
    for i, col in enumerate(columns):
        col_name = col[1]
        value = row[i]
        if value and len(str(value)) > 100:
            value = str(value)[:100] + "..."
        print(f"  {col_name:35s}: {value}")

conn_old.close()

# Now check current database
print("\n\n" + "=" * 80)
print("📊 CURRENT DATABASE (272 KB):")
print("-" * 80)

conn_current = sqlite3.connect(current_db_path)
cursor_current = conn_current.cursor()

# Get tables
cursor_current.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables_current = cursor_current.fetchall()

print(f"\nTables: {len(tables_current)}")
for table in tables_current:
    print(f"  - {table[0]}")

# Check residuos table
cursor_current.execute("PRAGMA table_info(residuos)")
columns_current = cursor_current.fetchall()

print(f"\n\n📋 RESIDUOS TABLE IN CURRENT DB:")
print(f"   Columns: {len(columns_current)}")

cursor_current.execute("SELECT COUNT(*) FROM residuos")
count_current = cursor_current.fetchone()[0]
print(f"   Rows: {count_current}")

conn_current.close()

# Compare
print("\n\n" + "=" * 80)
print("🔍 COMPARISON:")
print("=" * 80)

print(f"\nOLD DB:")
print(f"  Tables: {len(tables_old)}")
print(f"  Residuos columns: {len(columns_old)}")
print(f"  Residuos rows: {count_old}")

print(f"\nCURRENT DB:")
print(f"  Tables: {len(tables_current)}")
print(f"  Residuos columns: {len(columns_current)}")
print(f"  Residuos rows: {count_current}")

# Find missing columns
old_col_names = set([col[1] for col in columns_old])
current_col_names = set([col[1] for col in columns_current])

missing_in_current = old_col_names - current_col_names
missing_in_old = current_col_names - old_col_names

if missing_in_current:
    print(f"\n\n🔍 COLUMNS IN OLD DB NOT IN CURRENT ({len(missing_in_current)}):")
    print("-" * 80)
    for col in sorted(missing_in_current):
        print(f"  - {col}")

if missing_in_old:
    print(f"\n\n🔍 COLUMNS IN CURRENT DB NOT IN OLD ({len(missing_in_old)}):")
    print("-" * 80)
    for col in sorted(missing_in_old):
        print(f"  - {col}")

print("\n\n📝 NEXT STEP:")
print("=" * 80)
print("Based on this comparison, we'll create a merge script to:")
print("  1. Add any missing columns from old DB to current DB")
print("  2. Copy data that exists in old but not in current")
print("  3. Preserve all new data in current DB")
