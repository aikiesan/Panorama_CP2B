"""
Script para adicionar a função render_hierarchical_dropdowns() ao tabs.py
"""

# Nova função a ser adicionada
new_function = """

def render_hierarchical_dropdowns(key_prefix: str = "hierarchical") -> Optional[str]:
    \"\"\"
    Seletor hierárquico minimalista: Setor → Cultura → Resíduo

    Layout compacto com 3 dropdowns lado a lado (sem cards visuais).
    Phase 5: Integração do sistema hierárquico de culturas.

    Args:
        key_prefix: Unique prefix for component keys

    Returns:
        Selected residue name or None

    Example:
        >>> from src.ui.tabs import render_hierarchical_dropdowns
        >>> selected_residue = render_hierarchical_dropdowns(key_prefix="disp")
        >>> if selected_residue:
        ...     # Use residue data
    \"\"\"
    from src.data.culture_hierarchy import (
        get_cultures_by_sector,
        get_residues_by_culture,
        get_culture_icon
    )

    st.markdown("### 🎯 Selecione o Setor, Cultura e Resíduo")

    # Get all sectors
    sectors = get_all_sectors()
    all_sector_names = ["Agricultura", "Pecuária", "Urbano", "Industrial"]
    available_sectors = [name for name in all_sector_names if name in sectors and sectors[name].get("residues")]

    if not available_sectors:
        st.warning("⏳ Nenhum setor disponível no momento")
        return None

    # 3 columns for 3 dropdowns (compact layout)
    col1, col2, col3 = st.columns([1, 1, 1])

    # ========================================================================
    # DROPDOWN 1: SETOR
    # ========================================================================
    with col1:
        selected_sector = st.selectbox(
            "**🏭 Setor:**",
            all_sector_names,
            format_func=lambda x: f"{sectors[x]['icon']} {x}" if x in sectors else f"🔒 {x} (Em breve)",
            key=f"{key_prefix}_sector",
            help="Selecione o setor de origem dos resíduos"
        )

    # Check if sector is available
    if not selected_sector or selected_sector not in available_sectors:
        with col2:
            st.info("⏳ Setor em desenvolvimento")
        with col3:
            st.info("⏳ Aguardando seleção")
        return None

    # ========================================================================
    # DROPDOWN 2: CULTURA
    # ========================================================================
    with col2:
        cultures = get_cultures_by_sector(selected_sector)

        if not cultures:
            st.info(f"⏳ Nenhuma cultura disponível")
            with col3:
                st.info("⏳ Aguardando cultura")
            return None

        selected_culture = st.selectbox(
            "**🌾 Cultura:**",
            cultures,
            format_func=lambda x: f"{get_culture_icon(x)} {x}",
            key=f"{key_prefix}_culture_{selected_sector}",
            help="Selecione a cultura ou subsetor"
        )

    # ========================================================================
    # DROPDOWN 3: RESÍDUO
    # ========================================================================
    with col3:
        if not selected_culture:
            st.info("⏳ Aguardando cultura")
            return None

        residues = get_residues_by_culture(selected_sector, selected_culture)

        if not residues:
            st.info(f"⏳ Nenhum resíduo disponível")
            return None

        selected_residue = st.selectbox(
            "**📦 Resíduo:**",
            residues,
            format_func=lambda x: f"{get_residue_icon(x)} {x}",
            key=f"{key_prefix}_residue_{selected_sector}_{selected_culture}",
            help=f"Selecione o resíduo de {selected_culture}"
        )

        return selected_residue

    return None
"""

# Ler o arquivo
with open('src/ui/tabs.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar a nova função no final
if 'render_hierarchical_dropdowns' not in content:
    content += new_function
    print("[OK] Funcao render_hierarchical_dropdowns() adicionada")
else:
    print("[INFO] Funcao ja existe, pulando")

# Escrever de volta
with open('src/ui/tabs.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n[SUCCESS] Arquivo tabs.py atualizado!")
print("\nProximo passo: Modificar pagina Disponibilidade")
