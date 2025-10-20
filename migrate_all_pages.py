"""
Script para migrar TODAS as páginas restantes para o seletor hierárquico
Páginas: Parâmetros Químicos, Referências Científicas, Lab Comparação
"""

# Lista de páginas a migrar
pages_to_migrate = [
    {
        "file": "pages/2_🧪_Parametros_Quimicos.py",
        "key_prefix": "parametros",
        "name": "Parametros Quimicos"
    },
    {
        "file": "pages/3_📚_Referencias_Cientificas.py",
        "key_prefix": "referencias",
        "name": "Referencias Cientificas"
    },
    {
        "file": "pages/4_🔬_Comparacao_Laboratorial.py",
        "key_prefix": "lab_comp",
        "name": "Lab Comparacao"
    }
]

print("="*70)
print("MIGRACAO COMPLETA: Seletor Hierarquico para TODAS as Paginas")
print("="*70)

for page in pages_to_migrate:
    print(f"\n[PROCESSANDO] {page['name']}...")

    # Ler o arquivo
    try:
        with open(page['file'], 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  [ERRO] Nao foi possivel ler o arquivo: {e}")
        continue

    # 1. Atualizar import
    old_import = "from src.ui.tabs import render_sector_tabs"
    new_import = "from src.ui.tabs import render_sector_tabs, render_hierarchical_dropdowns"

    if old_import in content and new_import not in content:
        content = content.replace(old_import, new_import)
        print(f"  [OK] Import atualizado")
    elif new_import in content:
        print(f"  [SKIP] Import ja esta atualizado")
    else:
        print(f"  [WARN] Import nao encontrado")

    # 2. Substituir função
    old_code = f'selected_sector, selected_residue = render_sector_tabs(key_prefix="{page["key_prefix"]}")'
    new_code = f'selected_residue = render_hierarchical_dropdowns(key_prefix="{page["key_prefix"]}")'

    if old_code in content:
        content = content.replace(old_code, new_code)
        print(f"  [OK] Funcao substituida")
    elif new_code in content:
        print(f"  [SKIP] Funcao ja esta atualizada")
    else:
        print(f"  [WARN] Codigo exato nao encontrado, tentando alternativa...")
        # Alternativa: buscar padrão mais flexível
        import re
        pattern = rf'selected_sector,\s*selected_residue\s*=\s*render_sector_tabs\s*\(\s*key_prefix\s*=\s*"{page["key_prefix"]}"\s*\)'
        if re.search(pattern, content):
            content = re.sub(pattern, new_code, content)
            print(f"  [OK] Funcao substituida (regex)")
        else:
            print(f"  [ERROR] Nao foi possivel encontrar o codigo")
            continue

    # Escrever de volta
    try:
        with open(page['file'], 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [SUCCESS] Arquivo atualizado!")
    except Exception as e:
        print(f"  [ERRO] Nao foi possivel escrever o arquivo: {e}")

print("\n" + "="*70)
print("[COMPLETO] Migracao finalizada!")
print("="*70)
print("\nPaginas migradas:")
print("  1. Parametros Quimicos")
print("  2. Referencias Cientificas")
print("  3. Lab Comparacao")
print("\nTeste agora: http://localhost:8501")
print("Navegue para cada pagina e teste o seletor hierarquico!")
