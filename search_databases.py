
"""
Comprehensive Database File Search
Searches for all database files in CP2B project
"""

import os
from datetime import datetime
from pathlib import Path

print("🔍 COMPREHENSIVE DATABASE SEARCH - CP2B PROJECT")
print("=" * 80)

# Define search paths
search_paths = [
    r"C:\Users\Lucas\Documents\CP2B\PanoramaCP2B",
    r"C:\Users\Lucas\Documents\CP2B\Validacao_dados",
    r"C:\Users\Lucas\Documents\CP2B",  # Parent directory
]

# Also check common subdirectories
subdirs_to_check = [
    "data",
    "database", 
    "db",
    "backup",
    "backups",
    "webapp",
    "old",
    "archive",
]

db_files = []

for search_path in search_paths:
    print(f"\n📁 Searching in: {search_path}")
    print("-" * 80)
    
    if not os.path.exists(search_path):
        print("  ⚠️ Path does not exist")
        continue
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(search_path):
        for file in files:
            # Look for database files
            if file.endswith(('.db', '.sqlite', '.sqlite3', '.db3')):
                filepath = os.path.join(root, file)
                
                try:
                    file_size = os.path.getsize(filepath)
                    mod_time = os.path.getmtime(filepath)
                    mod_date = datetime.fromtimestamp(mod_time)
                    
                    db_files.append({
                        'path': filepath,
                        'name': file,
                        'size': file_size,
                        'modified': mod_date,
                        'size_kb': file_size / 1024,
                        'relative_path': os.path.relpath(filepath, search_path)
                    })
                    
                    print(f"  ✅ Found: {file}")
                    print(f"      Location: {os.path.relpath(filepath, search_path)}")
                    print(f"      Size: {file_size/1024:.1f} KB")
                    print(f"      Modified: {mod_date.strftime('%Y-%m-%d %H:%M:%S')}")
                except Exception as e:
                    print(f"  ❌ Error reading {file}: {e}")

print("\n\n" + "=" * 80)
print("📊 DATABASE FILES SUMMARY")
print("=" * 80)

if db_files:
    # Sort by modification date (newest first)
    db_files.sort(key=lambda x: x['modified'], reverse=True)
    
    print(f"\nTotal database files found: {len(db_files)}\n")
    
    # Categorize databases
    current_db = []
    backup_dbs = []
    old_dbs = []
    other_dbs = []
    
    for db in db_files:
        if 'cp2b_panorama.db' in db['name'] and 'BACKUP' not in db['name'].upper():
            current_db.append(db)
        elif 'BACKUP' in db['name'].upper() or 'backup' in db['path'].lower():
            backup_dbs.append(db)
        elif 'old' in db['path'].lower() or 'archive' in db['path'].lower():
            old_dbs.append(db)
        else:
            other_dbs.append(db)
    
    # Display categorized results
    if current_db:
        print("\n🎯 CURRENT PRODUCTION DATABASE:")
        print("-" * 80)
        for db in current_db:
            print(f"  File: {db['name']}")
            print(f"  Path: {db['path']}")
            print(f"  Size: {db['size_kb']:.1f} KB")
            print(f"  Modified: {db['modified'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    if backup_dbs:
        print(f"\n💾 BACKUP DATABASES ({len(backup_dbs)}):")
        print("-" * 80)
        for i, db in enumerate(backup_dbs[:10], 1):  # Show first 10
            age_days = (datetime.now() - db['modified']).days
            print(f"  {i:2d}. {db['name']:60s} | {db['size_kb']:7.1f} KB | {age_days:3d} days old")
        if len(backup_dbs) > 10:
            print(f"      ... and {len(backup_dbs)-10} more backups")
    
    if old_dbs:
        print(f"\n🗄️ OLD/ARCHIVED DATABASES ({len(old_dbs)}):")
        print("-" * 80)
        for db in old_dbs:
            print(f"  {db['name']:50s} | {db['size_kb']:7.1f} KB | {db['modified'].strftime('%Y-%m-%d')}")
            print(f"    → {db['path']}")
    
    if other_dbs:
        print(f"\n📁 OTHER DATABASE FILES ({len(other_dbs)}):")
        print("-" * 80)
        for db in other_dbs:
            print(f"  {db['name']:50s} | {db['size_kb']:7.1f} KB | {db['modified'].strftime('%Y-%m-%d')}")
            print(f"    → {db['path']}")
    
    # Look for potentially complete databases
    print("\n\n🔍 ANALYSIS: Looking for complete databases")
    print("=" * 80)
    
    larger_dbs = [db for db in db_files if db['size_kb'] > 300]
    
    if larger_dbs:
        print(f"\n✅ Found {len(larger_dbs)} databases larger than 300 KB:")
        print("   (These might contain the complete structure with literature)\n")
        for db in larger_dbs:
            print(f"  📊 {db['name']}")
            print(f"      Size: {db['size_kb']:.1f} KB")
            print(f"      Path: {db['path']}")
            print(f"      Modified: {db['modified'].strftime('%Y-%m-%d %H:%M:%S')}")
            print()
    else:
        print("\n⚠️ No databases larger than current found (260 KB)")
        print("   The Excel file is likely the most complete source")
    
    # Check if we can inspect a database structure
    print("\n\n🔬 INSPECTING DATABASE SCHEMA")
    print("=" * 80)
    
    if current_db:
        import sqlite3
        try:
            conn = sqlite3.connect(current_db[0]['path'])
            cursor = conn.cursor()
            
            cursor.execute("PRAGMA table_info(residuos)")
            columns = cursor.fetchall()
            
            print(f"\nCurrent production DB has {len(columns)} columns:\n")
            for col in columns:
                print(f"  - {col[1]:30s} ({col[2]})")
            
            conn.close()
        except Exception as e:
            print(f"  ⚠️ Could not inspect database: {e}")

else:
    print("\n⚠️ No database files found")

print("\n\n📝 RECOMMENDATION:")
print("=" * 80)
print("""
If no complete database was found:
  → The Excel file (dossie_final_residuos_*.xlsx) is the source of truth
  → Run expand_database.py to add all fields to cp2b_panorama.db
  
If a larger/complete database was found:
  → Compare its structure with current database
  → Decide whether to use it or merge data
""")
