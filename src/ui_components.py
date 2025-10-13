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

