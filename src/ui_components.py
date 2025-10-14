"""
UI Components Module - DRY Principle
Reusable Streamlit UI components for the biogas dashboard.
"""

import streamlit as st
import pandas as pd
from pathlib import Path


def load_css():
    """
    Loads and applies the premium CSS design system.
    Should be called once at the start of each page.
    """
    css_file = Path(__file__).parent.parent / "assets" / "styles.css"
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def render_kpi_cards(kpis: dict):
    """
    Renders KPI metrics in a row of columns.
    
    Args:
        kpis: Dictionary with KPI values
            - total_biogas: Total biogas potential
            - total_municipios: Number of municipalities
            - top_municipio: Name of top municipality
            - top_municipio_valor: Biogas value of top municipality
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🌱 Potencial Total de Biogás",
            value=f"{kpis['total_biogas']:,.0f} m³/ano",
            help="Somatório do potencial de biogás de todos os municípios filtrados"
        )
    
    with col2:
        st.metric(
            label="🏙️ Municípios",
            value=f"{kpis['total_municipios']:,}",
            help="Número de municípios considerados na análise"
        )
    
    with col3:
        st.metric(
            label="⭐ Maior Potencial",
            value=kpis['top_municipio'],
            delta=f"{kpis['top_municipio_valor']:,.0f} m³/ano",
            help="Município com maior potencial de biogás"
        )


def render_sector_kpis(kpis: dict):
    """
    Renders sector-specific KPI metrics.
    
    Args:
        kpis: Dictionary with sector KPI values
            - total_agricola: Agricultural biogas
            - total_pecuaria: Livestock biogas
            - total_urbano: Urban biogas
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🌾 Agricultura",
            value=f"{kpis['total_agricola']:,.0f} m³/ano",
            help="Potencial de biogás de resíduos agrícolas"
        )
    
    with col2:
        st.metric(
            label="🐄 Pecuária",
            value=f"{kpis['total_pecuaria']:,.0f} m³/ano",
            help="Potencial de biogás de resíduos pecuários"
        )
    
    with col3:
        st.metric(
            label="🏭 Urbano",
            value=f"{kpis['total_urbano']:,.0f} m³/ano",
            help="Potencial de biogás de resíduos urbanos (RSU e RPO)"
        )


def render_filters_sidebar(df: pd.DataFrame) -> dict:
    """
    Creates clean, intuitive filter controls in the sidebar.

    Args:
        df: Source DataFrame with all available data

    Returns:
        dict: Dictionary with selected filter values
    """
    st.sidebar.header("🔍 Filtros de Visualização")
    st.sidebar.markdown("Ajuste os filtros para explorar os dados")
    st.sidebar.markdown("---")

    # Sector filter - simplified
    st.sidebar.subheader("Por Setor")
    setores_selecionados = []
    if st.sidebar.checkbox("🌾 Agricultura", value=True):
        setores_selecionados.append('Agricultura')
    if st.sidebar.checkbox("🐄 Pecuária", value=True):
        setores_selecionados.append('Pecuária')
    if st.sidebar.checkbox("🏭 Urbano", value=True):
        setores_selecionados.append('Urbano')

    st.sidebar.markdown("---")

    # Potential category filter - simplified
    st.sidebar.subheader("Por Categoria de Potencial")
    categorias_selecionadas = []
    if st.sidebar.checkbox("🔴 Alto Potencial", value=True):
        categorias_selecionadas.append('ALTO')
    if st.sidebar.checkbox("🟡 Médio Potencial", value=True):
        categorias_selecionadas.append('MÉDIO')
    if st.sidebar.checkbox("🟢 Baixo Potencial", value=True):
        categorias_selecionadas.append('BAIXO')

    st.sidebar.markdown("---")

    # Population range filter - simplified
    st.sidebar.subheader("Por População")
    pop_min = int(df['populacao_2022'].min())
    pop_max = int(df['populacao_2022'].max())

    use_pop_filter = st.sidebar.checkbox("Filtrar por faixa populacional", value=False)

    if use_pop_filter:
        pop_range = st.sidebar.slider(
            "População (habitantes):",
            min_value=pop_min,
            max_value=pop_max,
            value=(pop_min, pop_max),
            format="%d"
        )
    else:
        pop_range = (pop_min, pop_max)

    st.sidebar.markdown("---")

    # Municipality search - simplified
    with st.sidebar.expander("🔎 Buscar Município Específico"):
        municipios_disponiveis = sorted(df['nome_municipio'].unique().tolist())
        municipio_busca = st.selectbox(
            "Digite ou selecione:",
            options=["Todos"] + municipios_disponiveis,
            index=0
        )
        municipios_selecionados = None if municipio_busca == "Todos" else [municipio_busca]

    return {
        'categorias': categorias_selecionadas if categorias_selecionadas else ['ALTO', 'MÉDIO', 'BAIXO'],
        'setores': setores_selecionados if setores_selecionados else ['Agricultura', 'Pecuária', 'Urbano'],
        'pop_range': pop_range,
        'municipios': municipios_selecionados
    }


def render_data_table(df: pd.DataFrame, title: str = "Dados", 
                      columns: list = None, format_dict: dict = None):
    """
    Renders a formatted dataframe with download button.
    
    Args:
        df: DataFrame to display
        title: Title for the table section
        columns: Specific columns to display (None = all)
        format_dict: Dictionary mapping column names to format strings
    """
    st.subheader(title)
    
    # Select columns if specified
    if columns:
        df_display = df[columns].copy()
    else:
        df_display = df.copy()
    
    # Apply formatting
    if format_dict:
        df_display = df_display.style.format(format_dict)
    
    # Display table
    st.dataframe(df_display, use_container_width=True, height=400)
    
    # Download button
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Baixar dados (CSV)",
        data=csv,
        file_name=f"{title.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )


def render_info_card(title: str, content: str, icon: str = "ℹ️"):
    """
    Renders an information card with custom styling.
    
    Args:
        title: Card title
        content: Card content text
        icon: Emoji icon for the card
    """
    st.markdown(
        f"""
        <div style="
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #2ecc71;
            margin: 10px 0;
        ">
            <h3 style="margin-top: 0;">{icon} {title}</h3>
            <p style="margin-bottom: 0;">{content}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_comparison_metrics(mun_data: pd.Series, state_avg: dict):
    """
    Renders comparison metrics between a municipality and state average.
    
    Args:
        mun_data: Series with municipality data
        state_avg: Dictionary with state average values
    """
    st.subheader("📊 Comparação com Média Estadual")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mun_total = mun_data.get('total_final_m_ano', 0)
        avg_total = state_avg.get('total_final_m_ano', 0)
        delta_pct = ((mun_total - avg_total) / avg_total * 100) if avg_total > 0 else 0
        
        st.metric(
            label="Potencial Total",
            value=f"{mun_total:,.0f} m³/ano",
            delta=f"{delta_pct:+.1f}% vs média",
            help="Comparado com a média estadual"
        )
    
    with col2:
        mun_pop = mun_data.get('populacao_2022', 0)
        avg_pop = state_avg.get('populacao_2022', 0)
        delta_pop_pct = ((mun_pop - avg_pop) / avg_pop * 100) if avg_pop > 0 else 0
        
        st.metric(
            label="População",
            value=f"{mun_pop:,.0f}",
            delta=f"{delta_pop_pct:+.1f}% vs média"
        )
    
    with col3:
        mun_dens = mun_data.get('densidade_demografica', 0)
        avg_dens = state_avg.get('densidade_demografica', 0)
        delta_dens_pct = ((mun_dens - avg_dens) / avg_dens * 100) if avg_dens > 0 else 0
        
        st.metric(
            label="Densidade Demográfica",
            value=f"{mun_dens:.1f} hab/km²",
            delta=f"{delta_dens_pct:+.1f}% vs média"
        )


def show_about_section():
    """
    Displays information about the dashboard and data sources.
    """
    with st.expander("ℹ️ Sobre este Dashboard"):
        st.markdown("""
        ### Panorama de Biogás - Estado de São Paulo

        Este dashboard apresenta o potencial de produção de biogás a partir de diferentes
        fontes de resíduos no Estado de São Paulo.

        **Setores Analisados:**
        - 🌾 **Agricultura**: Resíduos de cana-de-açúcar, soja, milho, café, citros e silvicultura
        - 🐄 **Pecuária**: Resíduos de bovinos, suínos, aves e piscicultura
        - 🏭 **Urbano**: Resíduos sólidos urbanos (RSU) e resíduos de poda e capina (RPO)

        **Fonte dos Dados**: Centro de Pesquisa para Inovação em Gases de Efeito Estufa (NIPE/UNICAMP)

        **Metodologia**: Os potenciais foram calculados com base em dados municipais de
        produção agrícola, rebanhos e população, aplicando fatores de conversão específicos
        para cada tipo de resíduo.
        """)


# ============================================================================
# PARALLEL SECTOR SELECTOR (CP2B v2.0)
# ============================================================================

def render_sector_selector(key_prefix: str = "sector") -> str:
    """
    Render parallel sector selection cards

    Args:
        key_prefix: Unique prefix for component keys

    Returns:
        Selected sector name or None
    """
    from src.research_data import get_all_sectors

    st.markdown("### 🎯 Selecionar Setor")
    st.markdown("Escolha o setor de origem dos resíduos para análise:")

    sectors = get_all_sectors()
    
    # Get all 4 sectors (including empty ones for future)
    all_sector_names = ["Agricultura", "Pecuária", "Urbano", "Industrial"]

    # Initialize session state
    session_key = f"{key_prefix}_selected"
    if session_key not in st.session_state:
        st.session_state[session_key] = None

    # Add smooth scroll JavaScript
    st.markdown("""
    <script>
    function smoothScrollDown() {
        window.scrollBy({
            top: 400,
            behavior: 'smooth'
        });
    }
    </script>
    """, unsafe_allow_html=True)

    # Create 4 compact cards in a single row
    cols = st.columns(4)

    for idx, sector_name in enumerate(all_sector_names):
        sector = sectors.get(sector_name)
        if not sector:
            continue

        with cols[idx]:
            # Check if sector has residues
            has_residues = len(sector["residues"]) > 0
            opacity_style = "" if has_residues else "opacity: 0.5;"
            cursor_style = "cursor: pointer;" if has_residues else "cursor: not-allowed;"
            
            # Ultra-compact sector card - using string concatenation to avoid f-string issues
            html_content = (
                f'<div id="sector_{sector_name}" style="'
                f'background: {sector["gradient"]}; '
                f'padding: 0.8rem 0.6rem; '
                f'border-radius: 12px; '
                f'border: 2px solid {sector["border_color"]}; '
                f'text-align: center; '
                f'min-height: 110px; '
                f'max-height: 110px; '
                f'box-shadow: 0 2px 4px rgba(0,0,0,0.06); '
                f'{cursor_style} '
                f'{opacity_style} '
                f'margin-bottom: 0.5rem; '
                f'display: flex; '
                f'flex-direction: column; '
                f'justify-content: center; '
                f'align-items: center; '
                f'transition: transform 0.2s, box-shadow 0.2s;">'
                f'<div style="font-size: 2.2rem; margin-bottom: 0.3rem; line-height: 1;">{sector["icon"]}</div>'
                f'<h4 style="color: {sector["color"]}; margin: 0.2rem 0; font-weight: 700; font-size: 0.95rem; line-height: 1.2; white-space: nowrap;">'
                f'{sector["name"]}'
                f'</h4>'
                f'<p style="color: #4b5563; font-size: 0.72rem; margin: 0.25rem 0; line-height: 1.3; max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">'
                f'{sector["description"][:28]}...'
                f'</p>'
                f'<p style="color: {sector["color"]}; font-size: 0.75rem; margin: 0.3rem 0 0 0; font-weight: 700;">'
                f'📊 {len(sector["residues"])} resíduos'
                f'</p>'
                f'</div>'
            )
            st.markdown(html_content, unsafe_allow_html=True)

            # Button to select this sector (only if has residues)
            if has_residues:
                if st.button(
                    f"✓ {sector['name']}",
                    key=f"{key_prefix}_btn_{sector_name}",
                    use_container_width=True,
                    type="primary" if st.session_state[session_key] == sector_name else "secondary"
                ):
                    st.session_state[session_key] = sector_name
                    # Inject JavaScript to scroll smoothly
                    st.markdown("""
                    <script>
                    setTimeout(function() {
                        window.scrollBy({
                            top: 350,
                            behavior: 'smooth'
                        });
                    }, 100);
                    </script>
                    """, unsafe_allow_html=True)
                    st.rerun()
            else:
                # Disabled button for future sectors
                st.button(
                    "🔒 Em breve",
                    key=f"{key_prefix}_btn_disabled_{sector_name}",
                    use_container_width=True,
                    disabled=True
                )

    # Add hover effect and button styling CSS
    st.markdown("""
    <style>
    /* Sector card hover effect */
    div[id^="sector_"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.12) !important;
    }
    
    /* Improve button styling */
    div[data-testid="stButton"] button {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 0.4rem 1rem;
        transition: all 0.2s ease;
        border: 2px solid transparent;
    }
    
    /* Primary button (selected sector) */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        border-color: #1e40af;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
    }
    
    div[data-testid="stButton"] button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(37, 99, 235, 0.3);
    }
    
    /* Secondary button (not selected) */
    div[data-testid="stButton"] button[kind="secondary"] {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        color: #374151;
        border-color: #d1d5db;
    }
    
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
        border-color: #9ca3af;
        transform: translateY(-1px);
    }
    
    /* Disabled button */
    div[data-testid="stButton"] button:disabled {
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        color: #9ca3af;
        border-color: #e5e7eb;
        cursor: not-allowed;
        opacity: 0.6;
    }
    </style>
    """, unsafe_allow_html=True)

    return st.session_state[session_key]


def render_residue_selector_for_sector(
    sector_name: str,
    key_prefix: str = "residue"
) -> str:
    """
    Render residue selection dropdown for a specific sector

    Args:
        sector_name: Name of the selected sector
        key_prefix: Unique prefix for component keys

    Returns:
        Selected residue name or None
    """
    from src.research_data import (
        get_sector_info,
        get_residues_by_sector,
        get_residue_icon
    )

    sector = get_sector_info(sector_name)
    if not sector:
        st.error(f"⚠️ Setor '{sector_name}' não encontrado")
        return None

    residues = get_residues_by_sector(sector_name)

    if not residues:
        st.info(f"ℹ️ Nenhum resíduo disponível para o setor **{sector_name}** ainda")
        return None

    # Display selected sector info
    st.markdown(f"""
    <div style='background: {sector["gradient"]};
                padding: 1.2rem;
                border-radius: 12px;
                border-left: 6px solid {sector["border_color"]};
                margin-bottom: 1.5rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
        <p style='margin: 0; color: {sector["color"]}; font-weight: 700; font-size: 1.1rem;'>
            {sector["icon"]} Setor Selecionado: {sector["name"]}
        </p>
        <p style='margin: 0.6rem 0 0 0; color: #4b5563; font-size: 0.95rem;'>
            {sector["description"]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Residue selector
    st.markdown("### 🌾 Selecionar Resíduo")

    selected_residue = st.selectbox(
        "**Resíduo/Cultura:**",
        residues,
        format_func=lambda x: f"{get_residue_icon(x)} {x}",
        key=f"{key_prefix}_select_{sector_name}"
    )

    return selected_residue


def render_full_selector(key_prefix: str = "selector") -> str:
    """
    Render complete sector + residue selector workflow with session state

    Args:
        key_prefix: Unique prefix for component keys

    Returns:
        Selected residue name or None
    """
    # Initialize session state
    sector_key = f"{key_prefix}_selected_sector"
    if sector_key not in st.session_state:
        st.session_state[sector_key] = None

    # Show sector selector
    selected_sector = render_sector_selector(key_prefix=f"{key_prefix}_sector")

    # Show residue selector if sector is selected
    if selected_sector or st.session_state[sector_key]:
        # Update session state
        if selected_sector:
            st.session_state[sector_key] = selected_sector

        st.markdown("---")

        # Button to change sector
        if st.button("🔄 Trocar Setor", key=f"{key_prefix}_change_sector"):
            st.session_state[sector_key] = None
            st.rerun()

        return render_residue_selector_for_sector(
            st.session_state[sector_key],
            key_prefix=f"{key_prefix}_residue"
        )

    return None


# ============================================================================
# PARAMETER RANGE VISUALIZATION (Elegant & Minimalist)
# ============================================================================

def render_compact_parameter_card(
    param_name: str,
    value: float,
    min_val: float = None,
    max_val: float = None,
    unit: str = "",
    icon: str = "📊"
) -> None:
    """
    Render single compact parameter card with optional range

    Args:
        param_name: Parameter name
        value: Current/mean value
        min_val: Minimum value (optional)
        max_val: Maximum value (optional)
        unit: Unit of measurement
        icon: Emoji icon
    """
    has_range = min_val is not None and max_val is not None

    if has_range:
        range_text = f"<span style='font-size: 0.75rem; color: #6b7280;'>Range: {min_val:.1f} - {max_val:.1f}</span>"
    else:
        range_text = ""

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
                padding: 1rem;
                border-radius: 10px;
                border: 1px solid #e5e7eb;
                text-align: center;
                min-height: 120px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
        <div style='font-size: 1.8rem; margin-bottom: 0.3rem;'>{icon}</div>
        <h4 style='color: #374151; margin: 0.3rem 0; font-weight: 600; font-size: 0.9rem;'>
            {param_name}
        </h4>
        <p style='color: #059669; font-size: 1.3rem; font-weight: 700; margin: 0.5rem 0;'>
            {value:.1f} {unit}
        </p>
        {range_text}
    </div>
    """, unsafe_allow_html=True)
