
"""
CP2B - Hierarchical Selector Debug & Fix
Run this to diagnose and fix the "Dados não encontrados" error
"""

import sqlite3
from pathlib import Path

print("🔍 DIAGNOSTIC: Hierarchical Selector Issue")
print("=" * 80)

# Connect to database
db_path = Path(__file__).parent / "data" / "cp2b_panorama.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Test 1: Check if get_residue_by_name works
print("\n✅ TEST 1: Testing get_residue_by_name()")
print("-" * 80)

from src.data_handler import get_residue_by_name

test_names = ['Bagaço de cana', 'Palha de cana', 'Lodo primário']

for name in test_names:
    result = get_residue_by_name(name)
    if result:
        print(f"✅ FOUND: '{name}' → codigo: {result.get('codigo', 'N/A')}")
    else:
        print(f"❌ NOT FOUND: '{name}'")

# Test 2: What does hierarchy return?
print("\n\n✅ TEST 2: What hierarchy returns for CANA")
print("-" * 80)

from src.data.hierarchy_helper import HierarchyHelper

helper = HierarchyHelper(str(db_path))
tree = helper.get_hierarchy_tree()

cana_residuos = tree['AG_AGRICULTURA']['subsetores']['CANA']['residuos']

print(f"CANA has {len(cana_residuos)} residuos:")
for r in cana_residuos:
    print(f"  - codigo: '{r['codigo']}' | nome: '{r['nome']}'")

# Test 3: Does the selector code work?
print("\n\n✅ TEST 3: Simulating selector logic")
print("-" * 80)

residuos = cana_residuos
residuo_options = [r['codigo'] for r in residuos]
residuo_labels = [r['nome'] for r in residuos]

print(f"residuo_options (codes): {residuo_options}")
print(f"residuo_labels (names): {residuo_labels}")

# Simulate selecting first item
selected_residuo_idx = 0
selected_residuo_nome = residuo_labels[selected_residuo_idx]

print(f"\nSelected index: {selected_residuo_idx}")
print(f"Selected name: '{selected_residuo_nome}'")

# Try to load
residue_data = get_residue_by_name(selected_residuo_nome)
if residue_data:
    print(f"✅ SUCCESS! Loaded: {residue_data.get('nome', 'N/A')}")
else:
    print(f"❌ FAILED! Could not load '{selected_residuo_nome}'")

conn.close()

print("\n\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
