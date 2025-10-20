"""
Script para atualizar a página Disponibilidade com o novo seletor hierárquico
"""

# Ler o arquivo
with open('pages/1_📊_Disponibilidade.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Atualizar o import na linha 18
old_import = "from src.ui.tabs import render_sector_tabs"
new_import = "from src.ui.tabs import render_sector_tabs, render_hierarchical_dropdowns"

if old_import in content:
    content = content.replace(old_import, new_import)
    print("[OK] Import atualizado")
else:
    print("[WARN] Import nao encontrado, tentando adicionar")

# Atualizar a linha 139 - mudando de render_sector_tabs para render_hierarchical_dropdowns
old_code = """    # Sector and residue selection
    selected_sector, selected_residue = render_sector_tabs(key_prefix="disponibilidade")"""

new_code = """    # Sector, culture and residue selection (Phase 5: Hierarchical)
    selected_residue = render_hierarchical_dropdowns(key_prefix="disponibilidade")"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("[OK] Codigo atualizado (linha 139)")
else:
    print("[WARN] Codigo exato nao encontrado")
    # Tentar alternativa mais flexível
    alt_old = "selected_sector, selected_residue = render_sector_tabs(key_prefix=\"disponibilidade\")"
    alt_new = "selected_residue = render_hierarchical_dropdowns(key_prefix=\"disponibilidade\")"
    if alt_old in content:
        content = content.replace(alt_old, alt_new)
        print("[OK] Codigo atualizado (alternativo)")

# Escrever de volta
with open('pages/1_📊_Disponibilidade.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n[SUCCESS] Pagina Disponibilidade atualizada!")
print("\nProximo passo: Testar a pagina")
print("Execute: streamlit run pages/1_📊_Disponibilidade.py")
