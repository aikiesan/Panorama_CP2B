"""
Script para atualizar src/ui/__init__.py com os novos imports de Phase 5
"""

import time

# Ler o arquivo
with open('src/ui/__init__.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Definir o texto a ser substituído
old_text = """# Selector Components
from .selector_components import (
    render_sector_selector,
    render_residue_selector_for_sector,
    render_full_selector
)

# Table Components"""

new_text = """# Selector Components
from .selector_components import (
    render_sector_selector,
    render_residue_selector_for_sector,
    render_full_selector
)

# Phase 5: Culture Hierarchy Selectors (3-Level: Sector -> Culture -> Residue)
from .culture_selector import (
    render_culture_selector,
    render_residue_selector_for_culture
)

from .hierarchical_selector import (
    render_full_selector_3_levels,
    render_quick_selector_with_hierarchy
)

# Table Components"""

# Substituir imports
if old_text in content:
    content = content.replace(old_text, new_text)
    print("[OK] Imports atualizados")
else:
    print("[WARN] Texto nao encontrado nos imports - tentando adicionar manualmente")

# Atualizar __all__
old_all = """    # Selectors
    'render_sector_selector',
    'render_residue_selector_for_sector',
    'render_full_selector',

    # Tables"""

new_all = """    # Selectors
    'render_sector_selector',
    'render_residue_selector_for_sector',
    'render_full_selector',

    # Phase 5: Culture Hierarchy (3-Level)
    'render_culture_selector',
    'render_residue_selector_for_culture',
    'render_full_selector_3_levels',
    'render_quick_selector_with_hierarchy',

    # Tables"""

if old_all in content:
    content = content.replace(old_all, new_all)
    print("[OK] __all__ atualizado")
else:
    print("[WARN] Texto nao encontrado no __all__")

# Escrever de volta
with open('src/ui/__init__.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n[SUCCESS] Arquivo src/ui/__init__.py atualizado com sucesso!")
print("\nProximo passo: Execute 'streamlit run test_hierarchical_selector.py'")
