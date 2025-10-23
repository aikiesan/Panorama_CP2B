"""
Page 2: Parâmetros Químicos e Operacionais
CP2B - Chemical composition analysis with literature ranges
DATABASE INTEGRATED - Phase 1.1 Complete
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import os

# Database integration (replaces residue_registry)
from src.data_handler import (
    get_all_residues_with_params,
    get_residue_by_name,
    get_residues_for_dropdown,
    load_residue_from_db,
    get_panorama_connection,
    load_parameter_sources_for_residue
)

# New visualization components
from src.ui.chart_components import (
    create_bmp_comparison_bar,
    create_parameter_boxplot
)

from src.ui.main_navigation import render_main_navigation, render_navigation_divider

# Phase 2 - Reference Integration
from src.ui.reference_components import render_source_traceability_badge


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Parâmetros Químicos - CP2B",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# HEADER
# ============================================================================

def render_header():
    """Render header for chemical parameters page"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; padding: 2.5rem; margin: -1rem -1rem 2rem -1rem;
                text-align: center; border-radius: 0 0 25px 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
        <h1 style='margin: 0; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;'>
            🧪 Parâmetros Químicos e Operacionais
        </h1>
        <p style='margin: 15px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 300;'>
            Composição Química • BMP • Parâmetros Operacionais
        </p>
        <div style='margin-top: 15px; font-size: 0.95rem; opacity: 0.8;'>
            📊 Valores de Literatura • 📈 Ranges Validados • ⚗️ Metodologia Conservadora • 🗄️ Database Integrado
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# DATABASE-DRIVEN DROPDOWN SELECTOR
# ============================================================================

def render_hierarchical_residue_selector():
    """Render 3-level hierarchical selector: Setor → Subsetor → Resíduo"""
    from src.data.hierarchy_helper import HierarchyHelper

    st.markdown("### 🎯 Selecione o Resíduo")

    helper = HierarchyHelper()
    tree = helper.get_hierarchy_tree()

    col1, col2, col3 = st.columns(3)

    with col1:
        setor_options = []
        setor_labels = []

        for setor_cod, setor_data in tree.items():
            setor_options.append(setor_cod)
            setor_labels.append(f"{setor_data['emoji']} {setor_data['nome']}")

        selected_setor_idx = st.selectbox(
            "Setor:",
            range(len(setor_options)),
            format_func=lambda x: setor_labels[x],
            key="parametros_setor_selector"
        )

        selected_setor = setor_options[selected_setor_idx]

    with col2:
        subsetor_options = []
        subsetor_labels = []

        for subsetor_cod, subsetor_data in tree[selected_setor]['subsetores'].items():
            subsetor_options.append(subsetor_cod)
            residuo_count = len(subsetor_data['residuos'])
            subsetor_labels.append(f"{subsetor_data['nome']} ({residuo_count})")

        selected_subsetor_idx = st.selectbox(
            "Subsetor:",
            range(len(subsetor_options)),
            format_func=lambda x: subsetor_labels[x],
            key="parametros_subsetor_selector"
        )

        selected_subsetor = subsetor_options[selected_subsetor_idx]

    with col3:
        residuos = tree[selected_setor]['subsetores'][selected_subsetor]['residuos']

        residuo_options = [r['codigo'] for r in residuos]
        residuo_labels = [r['nome'] for r in residuos]

        selected_residuo_idx = st.selectbox(
            "Resíduo:",
            range(len(residuo_options)),
            format_func=lambda x: residuo_labels[x],
            key="parametros_residuo_selector"
        )

        selected_residuo_codigo = residuo_options[selected_residuo_idx]

    # Load full residue data from database using codigo
    residue_data = load_residue_from_db(selected_residuo_codigo)

    return residue_data



# ============================================================================
# PARAMETER SOURCES (PHASE 2 - REFERENCE INTEGRATION)
# ============================================================================

def render_parameter_sources_section(residue_data):
    """
    Render Ver Fontes section for parameters with source traceability.
    Phase 2 - Shows scientific papers and page numbers for each parameter.
    """
    residue_codigo = residue_data.get('codigo')

    if not residue_codigo:
        return

    st.markdown("---")
    st.markdown("### 📄 Referências Científicas por Parâmetro")
    st.info("""
    **Rastreabilidade completa**: Cada valor acima é rastreável até a fonte científica original.
    Clique em "Ver Fontes" para ver os papers de onde os dados foram extraídos.
    """)

    # Create tabs for each parameter
    tab_labels = ["💨 BMP", "📦 TS", "🔥 VS", "⚖️ C:N", "🌬️ CH₄"]
    tab_params = ["BMP", "TS", "VS", "CN_RATIO", "CH4"]

    tabs = st.tabs(tab_labels)

    for tab, param_name in zip(tabs, tab_params):
        with tab:
            render_single_parameter_sources(residue_codigo, param_name)


def render_single_parameter_sources(residue_codigo: str, parameter_name: str):
    """
    Render sources for a single parameter.

    Args:
        residue_codigo: Residue code (e.g., 'CANA_VINHACA')
        parameter_name: Parameter name (e.g., 'BMP', 'TS', 'VS')
    """
    # Load sources
    sources = load_parameter_sources_for_residue(residue_codigo, parameter_name)

    if not sources:
        st.warning(f"⚠️ Nenhuma fonte disponível para {parameter_name} neste resíduo.")
        st.caption("Os valores mostrados acima podem ser de fontes genéricas ou estimados.")
        return

    # Display count and quality summary
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📚 Fontes Encontradas", len(sources))

    with col2:
        high_quality = sum(1 for s in sources if s.data_quality.lower() == 'high')
        st.metric("⭐ Alta Qualidade", f"{high_quality}/{len(sources)}")

    with col3:
        with_pages = sum(1 for s in sources if s.page_number is not None)
        st.metric("📖 Com Página", f"{with_pages}/{len(sources)}")

    st.markdown("---")

    # Display sources (show first 5, then expandable for rest)
    display_limit = 5

    for idx, source in enumerate(sources[:display_limit]):
        render_source_card(source, idx)

    # Expandable section for remaining sources
    if len(sources) > display_limit:
        with st.expander(f"📄 Ver mais {len(sources) - display_limit} fonte(s)"):
            for idx, source in enumerate(sources[display_limit:], start=display_limit):
                render_source_card(source, idx)


def render_source_card(source, index: int):
    """
    Render a value-first compact card.

    Priority order: 1) Value, 2) Reference, 3) Access button

    Args:
        source: ParameterSource object
        index: Index for unique keys
    """
    # Row 1: VALUE (prominent, largest) | BUTTON (action)
    col1, col2 = st.columns([5, 2])

    with col1:
        # PRIMARY: VALUE - This is what researchers need most
        value_text = source.value_display if hasattr(source, 'value_display') else f"{source.value_mean} {source.unit}"
        st.markdown(f"### {value_text}")

    with col2:
        # Action button (aligned with value)
        pdf_path = Path(source.reference.pdf_path) if source.reference.pdf_path else None

        if pdf_path and pdf_path.exists():
            file_url = pdf_path.as_uri()
            st.link_button("📄 Ver Paper", file_url, use_container_width=True)
        elif source.reference.doi:
            doi_url = f"https://doi.org/{source.reference.doi}"
            st.link_button("🔗 Ver DOI", doi_url, use_container_width=True)

    # Row 2: SECONDARY: Citation source (establishes credibility)
    page_info = f", p. {source.page_number}" if source.page_number else ""
    st.markdown(f"**Fonte:** {source.reference.citation_short}{page_info}")

    # Row 3: Title (subtle, italic, provides context)
    if source.reference.title:
        title_short = source.reference.title[:80] + "..." if len(source.reference.title) > 80 else source.reference.title
        st.caption(f"_{title_short}_")

    # Row 4: Context excerpt (optional, only if present and useful)
    if source.measurement_conditions:
        context_short = source.measurement_conditions[:120] + "..." if len(source.measurement_conditions) > 120 else source.measurement_conditions
        st.caption(f"💬 {context_short}")

    # Subtle divider
    st.divider()


# ============================================================================
# CHEMICAL PARAMETERS DISPLAY (FROM DATABASE)
# ============================================================================

def render_chemical_parameters_from_db(residue_data):
    """Display chemical parameters from database dict structure"""
    st.markdown("### 🧬 Parâmetros de Composição (Literatura Validada)")

    st.info("""
    **📊 Como interpretar a tabela:**
    - **Mínimo**: Valor mínimo encontrado na literatura revisada
    - **Média/Valor**: Valor conservador adotado no CP2B (baseado em média ponderada)
    - **Máximo**: Valor máximo encontrado na literatura revisada
    - **Unidade**: Unidade de medida do parâmetro
    """)

    # Build table from database columns
    params_data = []

    # BMP
    params_data.append({
        "Parâmetro": "💨 BMP (Potencial Metanogênico)",
        "Mínimo": f"{residue_data.get('bmp_min', 0):.1f}" if pd.notna(residue_data.get('bmp_min')) else "N/A",
        "Média/Valor": f"{residue_data.get('bmp_medio', 0):.1f}",
        "Máximo": f"{residue_data.get('bmp_max', 0):.1f}" if pd.notna(residue_data.get('bmp_max')) else "N/A",
        "Unidade": "mL CH₄/g VS"
    })

    # TS (Sólidos Totais) / Dry Matter
    ts_value = residue_data.get('ts_medio', 0)
    params_data.append({
        "Parâmetro": "📦 TS (Sólidos Totais / Matéria Seca)",
        "Mínimo": f"{residue_data.get('ts_min', 0):.1f}" if pd.notna(residue_data.get('ts_min')) else "N/A",
        "Média/Valor": f"{ts_value:.1f}",
        "Máximo": f"{residue_data.get('ts_max', 0):.1f}" if pd.notna(residue_data.get('ts_max')) else "N/A",
        "Unidade": "%"
    })

    # Moisture Content (calculated from TS)
    if ts_value > 0:
        moisture_value = 100 - ts_value
        ts_min = residue_data.get('ts_min', 0)
        ts_max = residue_data.get('ts_max', 0)

        # Calculate moisture min/max (inverse of TS)
        moisture_max = f"{100 - ts_min:.1f}" if pd.notna(ts_min) and ts_min > 0 else "N/A"
        moisture_min = f"{100 - ts_max:.1f}" if pd.notna(ts_max) and ts_max > 0 else "N/A"

        params_data.append({
            "Parâmetro": "💧 Umidade (Moisture Content)",
            "Mínimo": moisture_min,
            "Média/Valor": f"{moisture_value:.1f}",
            "Máximo": moisture_max,
            "Unidade": "%"
        })

    # VS (Sólidos Voláteis)
    params_data.append({
        "Parâmetro": "🔥 VS (Sólidos Voláteis)",
        "Mínimo": f"{residue_data.get('vs_min', 0):.1f}" if pd.notna(residue_data.get('vs_min')) else "N/A",
        "Média/Valor": f"{residue_data.get('vs_medio', 0):.1f}",
        "Máximo": f"{residue_data.get('vs_max', 0):.1f}" if pd.notna(residue_data.get('vs_max')) else "N/A",
        "Unidade": "% (base TS)"
    })

    # C:N Ratio (if available)
    cn_ratio = residue_data.get('chemical_cn_ratio')
    if pd.notna(cn_ratio) and cn_ratio > 0:
        params_data.append({
            "Parâmetro": "⚖️ Relação C:N",
            "Mínimo": "N/A",
            "Média/Valor": f"{cn_ratio:.1f}",
            "Máximo": "N/A",
            "Unidade": "C:N"
        })

    # CH4 Content (if available)
    ch4_content = residue_data.get('chemical_ch4_content')
    if pd.notna(ch4_content) and ch4_content > 0:
        params_data.append({
            "Parâmetro": "🌬️ Conteúdo de CH₄ no Biogás",
            "Mínimo": "N/A",
            "Média/Valor": f"{ch4_content:.1f}",
            "Máximo": "N/A",
            "Unidade": "%"
        })

    df = pd.DataFrame(params_data)

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        height=280,
        column_config={
            "Parâmetro": st.column_config.TextColumn("Parâmetro", width="large"),
            "Mínimo": st.column_config.TextColumn("Mínimo", width="small"),
            "Média/Valor": st.column_config.TextColumn("Média/Valor ✅", width="small"),
            "Máximo": st.column_config.TextColumn("Máximo", width="small"),
            "Unidade": st.column_config.TextColumn("Unidade", width="medium"),
        }
    )

    # Phase 2 - Source Traceability
    render_parameter_sources_section(residue_data)

    # Enhanced key metrics (will be replaced by render_enhanced_metrics in main())


# ============================================================================
# RADAR CHART VISUALIZATION
# ============================================================================

def render_radar_chart(residue_data, df_all):
    """Create multi-dimensional radar chart comparing residue to sector average"""
    st.markdown("### 🎯 Análise Multi-Dimensional - Radar Chart")

    # Get sector for the selected residue
    residue_sector = residue_data.get('setor')

    # Calculate sector averages
    sector_df = df_all[df_all['setor'] == residue_sector]

    if sector_df.empty:
        st.warning("⚠️ Não há dados suficientes para comparação setorial")
        return

    # Get values for selected residue
    bmp_value = residue_data.get('bmp_medio', 0)
    ts_value = residue_data.get('ts_medio', 0)
    vs_value = residue_data.get('vs_medio', 0)
    cn_value = residue_data.get('chemical_cn_ratio', 0)
    ch4_value = residue_data.get('chemical_ch4_content', 0)

    # Get sector averages
    bmp_avg = sector_df['bmp_medio'].mean()
    ts_avg = sector_df['ts_medio'].mean()
    vs_avg = sector_df['vs_medio'].mean()
    cn_avg = sector_df['chemical_cn_ratio'].mean() if 'chemical_cn_ratio' in sector_df.columns else 0
    ch4_avg = sector_df['chemical_ch4_content'].mean() if 'chemical_ch4_content' in sector_df.columns else 0

    # Normalize values to 0-100 scale for radar chart
    def normalize(value, avg, parameter_type='bmp'):
        if avg == 0 or pd.isna(avg) or value == 0 or pd.isna(value):
            return 0

        # For BMP, TS, VS, CH4: higher is better, scale to percentage of average
        if parameter_type in ['bmp', 'ts', 'vs', 'ch4']:
            return min(100, (value / avg) * 100)

        # For C:N: optimal range is 20-30, scale accordingly
        elif parameter_type == 'cn':
            optimal_cn = 25
            deviation = abs(value - optimal_cn)
            return max(0, 100 - (deviation * 3))  # Penalize deviation from optimal

        return 50  # Default

    # Prepare data for radar chart
    categories = []
    residue_values = []
    sector_values = []

    # BMP
    if bmp_value > 0:
        categories.append('BMP')
        residue_values.append(normalize(bmp_value, bmp_avg, 'bmp'))
        sector_values.append(100)  # Sector average is baseline

    # TS
    if ts_value > 0:
        categories.append('Sólidos Totais')
        residue_values.append(normalize(ts_value, ts_avg, 'ts'))
        sector_values.append(100)

    # VS
    if vs_value > 0:
        categories.append('Sólidos Voláteis')
        residue_values.append(normalize(vs_value, vs_avg, 'vs'))
        sector_values.append(100)

    # C:N
    if cn_value > 0 and not pd.isna(cn_avg) and cn_avg > 0:
        categories.append('Relação C:N')
        residue_values.append(normalize(cn_value, cn_avg, 'cn'))
        sector_values.append(normalize(cn_avg, cn_avg, 'cn'))

    # CH4
    if ch4_value > 0 and not pd.isna(ch4_avg) and ch4_avg > 0:
        categories.append('CH₄ Content')
        residue_values.append(normalize(ch4_value, ch4_avg, 'ch4'))
        sector_values.append(100)

    if len(categories) < 3:
        st.info("ℹ️ Dados insuficientes para gerar radar chart (mínimo 3 parâmetros)")
        return

    # Create radar chart
    fig = go.Figure()

    # Add sector average trace
    fig.add_trace(go.Scatterpolar(
        r=sector_values,
        theta=categories,
        fill='toself',
        name='Média do Setor',
        line=dict(color='rgba(100, 100, 100, 0.5)', dash='dash', width=2),
        fillcolor='rgba(100, 100, 100, 0.1)'
    ))

    # Add residue trace
    fig.add_trace(go.Scatterpolar(
        r=residue_values,
        theta=categories,
        fill='toself',
        name=residue_data.get('nome', 'Resíduo Selecionado'),
        line=dict(color='#667eea', width=3),
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 120],
                ticksuffix='%',
                showgrid=True
            )
        ),
        showlegend=True,
        height=500,
        title=dict(
            text=f"Comparação Multi-Dimensional - {residue_data.get('nome', 'N/A')} vs Média Setorial",
            x=0.5,
            xanchor='center'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(f"""
    **📊 Como interpretar:**
    - **Linha sólida azul**: Valores do resíduo selecionado (normalizado vs média setorial)
    - **Linha tracejada cinza**: Média do setor {residue_sector}
    - **100%**: Igual à média setorial
    - **>100%**: Acima da média setorial (geralmente melhor)
    - **<100%**: Abaixo da média setorial
    """)


# ============================================================================
# SECTOR COMPARISON BARS
# ============================================================================

def render_sector_comparison_bars(residue_data, df_all):
    """Create comparison bars showing residue vs sector average for each parameter"""
    st.markdown("### 📊 Comparação com Média Setorial")

    # Get sector for the selected residue
    residue_sector = residue_data.get('setor')

    # Calculate sector averages
    sector_df = df_all[df_all['setor'] == residue_sector]

    if sector_df.empty:
        st.warning("⚠️ Não há dados suficientes para comparação setorial")
        return

    # Get sector averages
    sector_stats = {
        'bmp': sector_df['bmp_medio'].mean(),
        'ts': sector_df['ts_medio'].mean(),
        'vs': sector_df['vs_medio'].mean(),
        'cn': sector_df['chemical_cn_ratio'].mean() if 'chemical_cn_ratio' in sector_df.columns else None,
        'ch4': sector_df['chemical_ch4_content'].mean() if 'chemical_ch4_content' in sector_df.columns else None
    }

    # Create comparison data
    comparison_data = []

    # BMP
    bmp_value = residue_data.get('bmp_medio', 0)
    if bmp_value > 0 and sector_stats['bmp'] > 0:
        delta_pct = ((bmp_value - sector_stats['bmp']) / sector_stats['bmp']) * 100
        comparison_data.append({
            'Parâmetro': 'BMP',
            'Resíduo': bmp_value,
            'Média Setor': sector_stats['bmp'],
            'Delta (%)': delta_pct,
            'Status': 'Acima' if delta_pct > 5 else ('Abaixo' if delta_pct < -5 else 'Similar')
        })

    # TS
    ts_value = residue_data.get('ts_medio', 0)
    if ts_value > 0 and sector_stats['ts'] > 0:
        delta_pct = ((ts_value - sector_stats['ts']) / sector_stats['ts']) * 100
        comparison_data.append({
            'Parâmetro': 'Sólidos Totais',
            'Resíduo': ts_value,
            'Média Setor': sector_stats['ts'],
            'Delta (%)': delta_pct,
            'Status': 'Acima' if delta_pct > 5 else ('Abaixo' if delta_pct < -5 else 'Similar')
        })

    # VS
    vs_value = residue_data.get('vs_medio', 0)
    if vs_value > 0 and sector_stats['vs'] > 0:
        delta_pct = ((vs_value - sector_stats['vs']) / sector_stats['vs']) * 100
        comparison_data.append({
            'Parâmetro': 'Sólidos Voláteis',
            'Resíduo': vs_value,
            'Média Setor': sector_stats['vs'],
            'Delta (%)': delta_pct,
            'Status': 'Acima' if delta_pct > 5 else ('Abaixo' if delta_pct < -5 else 'Similar')
        })

    # C:N
    cn_value = residue_data.get('chemical_cn_ratio', 0)
    if cn_value > 0 and sector_stats['cn'] and not pd.isna(sector_stats['cn']) and sector_stats['cn'] > 0:
        delta_pct = ((cn_value - sector_stats['cn']) / sector_stats['cn']) * 100
        comparison_data.append({
            'Parâmetro': 'Relação C:N',
            'Resíduo': cn_value,
            'Média Setor': sector_stats['cn'],
            'Delta (%)': delta_pct,
            'Status': 'Acima' if delta_pct > 5 else ('Abaixo' if delta_pct < -5 else 'Similar')
        })

    # CH4
    ch4_value = residue_data.get('chemical_ch4_content', 0)
    if ch4_value > 0 and sector_stats['ch4'] and not pd.isna(sector_stats['ch4']) and sector_stats['ch4'] > 0:
        delta_pct = ((ch4_value - sector_stats['ch4']) / sector_stats['ch4']) * 100
        comparison_data.append({
            'Parâmetro': 'CH₄ Content',
            'Resíduo': ch4_value,
            'Média Setor': sector_stats['ch4'],
            'Delta (%)': delta_pct,
            'Status': 'Acima' if delta_pct > 5 else ('Abaixo' if delta_pct < -5 else 'Similar')
        })

    if not comparison_data:
        st.info("ℹ️ Dados insuficientes para comparação setorial")
        return

    df_comparison = pd.DataFrame(comparison_data)

    # Create grouped bar chart
    fig = go.Figure()

    # Add residue bars
    fig.add_trace(go.Bar(
        name='Resíduo Selecionado',
        x=df_comparison['Parâmetro'],
        y=df_comparison['Resíduo'],
        marker_color='#667eea',
        text=df_comparison['Resíduo'].round(1),
        textposition='outside',
        texttemplate='%{text}'
    ))

    # Add sector average bars
    fig.add_trace(go.Bar(
        name='Média do Setor',
        x=df_comparison['Parâmetro'],
        y=df_comparison['Média Setor'],
        marker_color='rgba(100, 100, 100, 0.5)',
        text=df_comparison['Média Setor'].round(1),
        textposition='outside',
        texttemplate='%{text}'
    ))

    fig.update_layout(
        title=f"Comparação - {residue_data.get('nome', 'N/A')} vs Média do Setor",
        xaxis_title="Parâmetro",
        yaxis_title="Valor",
        barmode='group',
        height=450,
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # Show delta table
    with st.expander("📈 Ver diferenças percentuais detalhadas"):
        delta_df = df_comparison[['Parâmetro', 'Delta (%)', 'Status']].copy()
        delta_df['Delta (%)'] = delta_df['Delta (%)'].round(1)

        # Color code status
        def color_status(val):
            if val == 'Acima':
                return 'background-color: rgba(16, 185, 129, 0.2)'  # Green
            elif val == 'Abaixo':
                return 'background-color: rgba(245, 158, 11, 0.2)'  # Orange
            else:
                return 'background-color: rgba(100, 100, 100, 0.1)'  # Gray

        styled_df = delta_df.style.applymap(color_status, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True)


# ============================================================================
# ENHANCED METRICS CARDS
# ============================================================================

def render_enhanced_metrics(residue_data, df_all):
    """Render enhanced metric cards with color coding, ranks, and deltas"""
    st.markdown("### 📌 Destaques - Métricas Principais")

    # Get sector for the selected residue
    residue_sector = residue_data.get('setor')
    sector_df = df_all[df_all['setor'] == residue_sector]

    # Calculate sector statistics
    sector_stats = {}
    if not sector_df.empty:
        sector_stats = {
            'bmp_avg': sector_df['bmp_medio'].mean(),
            'ts_avg': sector_df['ts_medio'].mean(),
            'vs_avg': sector_df['vs_medio'].mean(),
        }

        # Calculate rank within sector
        sector_df_sorted = sector_df.sort_values('bmp_medio', ascending=False).reset_index(drop=True)
        residue_code = residue_data.get('codigo')
        if residue_code:
            rank_bmp = sector_df_sorted[sector_df_sorted['codigo'] == residue_code].index[0] + 1 if residue_code in sector_df_sorted['codigo'].values else None
        else:
            rank_bmp = None

        sector_stats['bmp_rank'] = rank_bmp
        sector_stats['bmp_total'] = len(sector_df)

    # Create enhanced metric cards
    col1, col2, col3, col4 = st.columns(4)

    # BMP Card
    with col1:
        bmp_value = residue_data.get('bmp_medio', 0)

        # Calculate delta vs sector average
        if sector_stats and sector_stats.get('bmp_avg'):
            delta_bmp = bmp_value - sector_stats['bmp_avg']
            delta_pct = (delta_bmp / sector_stats['bmp_avg']) * 100

            # Determine color
            if delta_pct > 10:
                color = "#10b981"  # Green
            elif delta_pct < -10:
                color = "#f59e0b"  # Orange
            else:
                color = "#667eea"  # Blue

            # Rank badge
            rank_text = ""
            if sector_stats.get('bmp_rank'):
                rank_text = f"#{sector_stats['bmp_rank']}/{sector_stats['bmp_total']} no setor"

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {color}20, {color}40);
                        padding: 1.2rem; border-radius: 12px; border-left: 4px solid {color};'>
                <div style='font-size: 0.85rem; color: {color}; font-weight: 600; margin-bottom: 0.5rem;'>
                    💨 BMP
                </div>
                <div style='font-size: 2rem; font-weight: 700; color: {color}; margin-bottom: 0.3rem;'>
                    {bmp_value:.1f}
                </div>
                <div style='font-size: 0.75rem; color: #666; margin-bottom: 0.5rem;'>
                    mL CH₄/g VS
                </div>
                <div style='font-size: 0.8rem; color: {color}; font-weight: 500;'>
                    {delta_pct:+.1f}% vs setor
                </div>
                <div style='font-size: 0.7rem; color: #888; margin-top: 0.3rem;'>
                    {rank_text}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.metric("💨 BMP", f"{bmp_value:.1f}", help="mL CH₄/g VS")

    # TS Card
    with col2:
        ts_value = residue_data.get('ts_medio', 0)

        if sector_stats and sector_stats.get('ts_avg'):
            delta_ts = ts_value - sector_stats['ts_avg']
            delta_pct = (delta_ts / sector_stats['ts_avg']) * 100

            color = "#10b981" if delta_pct > 5 else ("#f59e0b" if delta_pct < -5 else "#667eea")

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {color}20, {color}40);
                        padding: 1.2rem; border-radius: 12px; border-left: 4px solid {color};'>
                <div style='font-size: 0.85rem; color: {color}; font-weight: 600; margin-bottom: 0.5rem;'>
                    📦 Sólidos Totais
                </div>
                <div style='font-size: 2rem; font-weight: 700; color: {color}; margin-bottom: 0.3rem;'>
                    {ts_value:.1f}%
                </div>
                <div style='font-size: 0.75rem; color: #666; margin-bottom: 0.5rem;'>
                    Total Solids
                </div>
                <div style='font-size: 0.8rem; color: {color}; font-weight: 500;'>
                    {delta_pct:+.1f}% vs setor
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.metric("📦 Sólidos Totais", f"{ts_value:.1f}%")

    # Moisture Card
    with col3:
        moisture = 100 - ts_value if ts_value > 0 else 0

        if sector_stats and sector_stats.get('ts_avg'):
            sector_moisture = 100 - sector_stats['ts_avg']
            delta_moisture = moisture - sector_moisture
            delta_pct = (delta_moisture / sector_moisture) * 100 if sector_moisture > 0 else 0

            # For moisture, lower might be better in some cases
            color = "#667eea"

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {color}20, {color}40);
                        padding: 1.2rem; border-radius: 12px; border-left: 4px solid {color};'>
                <div style='font-size: 0.85rem; color: {color}; font-weight: 600; margin-bottom: 0.5rem;'>
                    💧 Umidade
                </div>
                <div style='font-size: 2rem; font-weight: 700; color: {color}; margin-bottom: 0.3rem;'>
                    {moisture:.1f}%
                </div>
                <div style='font-size: 0.75rem; color: #666; margin-bottom: 0.5rem;'>
                    Moisture Content
                </div>
                <div style='font-size: 0.8rem; color: {color}; font-weight: 500;'>
                    {delta_pct:+.1f}% vs setor
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.metric("💧 Umidade", f"{moisture:.1f}%")

    # VS Card
    with col4:
        vs_value = residue_data.get('vs_medio', 0)

        if sector_stats and sector_stats.get('vs_avg'):
            delta_vs = vs_value - sector_stats['vs_avg']
            delta_pct = (delta_vs / sector_stats['vs_avg']) * 100

            color = "#10b981" if delta_pct > 5 else ("#f59e0b" if delta_pct < -5 else "#667eea")

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {color}20, {color}40);
                        padding: 1.2rem; border-radius: 12px; border-left: 4px solid {color};'>
                <div style='font-size: 0.85rem; color: {color}; font-weight: 600; margin-bottom: 0.5rem;'>
                    🔥 Sólidos Voláteis
                </div>
                <div style='font-size: 2rem; font-weight: 700; color: {color}; margin-bottom: 0.3rem;'>
                    {vs_value:.1f}%
                </div>
                <div style='font-size: 0.75rem; color: #666; margin-bottom: 0.5rem;'>
                    Volatile Solids
                </div>
                <div style='font-size: 0.8rem; color: {color}; font-weight: 500;'>
                    {delta_pct:+.1f}% vs setor
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.metric("🔥 Sólidos Voláteis", f"{vs_value:.1f}%")


# ============================================================================
# LITERATURE REFERENCES DISPLAY
# ============================================================================

def render_literature_references(residue_data):
    """Display literature references and summaries if available"""
    # Check if any literature data exists
    has_literature = False
    literature_items = []

    # Check BMP literature
    bmp_resumo = residue_data.get('bmp_resumo_literatura')
    bmp_refs = residue_data.get('bmp_referencias_literatura')
    if pd.notna(bmp_resumo) and str(bmp_resumo).strip():
        has_literature = True
        literature_items.append({
            'parameter': 'BMP (Potencial Metanogênico)',
            'summary': str(bmp_resumo),
            'references': str(bmp_refs) if pd.notna(bmp_refs) else None
        })

    # Check TS literature
    ts_resumo = residue_data.get('ts_resumo_literatura')
    ts_refs = residue_data.get('ts_referencias_literatura')
    if pd.notna(ts_resumo) and str(ts_resumo).strip():
        has_literature = True
        literature_items.append({
            'parameter': 'TS (Sólidos Totais)',
            'summary': str(ts_resumo),
            'references': str(ts_refs) if pd.notna(ts_refs) else None
        })

    # Check VS literature
    vs_resumo = residue_data.get('vs_resumo_literatura')
    vs_refs = residue_data.get('vs_referencias_literatura')
    if pd.notna(vs_resumo) and str(vs_resumo).strip():
        has_literature = True
        literature_items.append({
            'parameter': 'VS (Sólidos Voláteis)',
            'summary': str(vs_resumo),
            'references': str(vs_refs) if pd.notna(vs_refs) else None
        })

    # Check C:N literature
    cn_resumo = residue_data.get('cn_resumo_literatura')
    cn_refs = residue_data.get('cn_referencias_literatura')
    if pd.notna(cn_resumo) and str(cn_resumo).strip():
        has_literature = True
        literature_items.append({
            'parameter': 'C:N (Relação Carbono:Nitrogênio)',
            'summary': str(cn_resumo),
            'references': str(cn_refs) if pd.notna(cn_refs) else None
        })

    # Check CH4 literature
    ch4_resumo = residue_data.get('ch4_resumo_literatura')
    ch4_refs = residue_data.get('ch4_referencias_literatura')
    if pd.notna(ch4_resumo) and str(ch4_resumo).strip():
        has_literature = True
        literature_items.append({
            'parameter': 'CH₄ (Conteúdo de Metano)',
            'summary': str(ch4_resumo),
            'references': str(ch4_refs) if pd.notna(ch4_refs) else None
        })

    if not has_literature:
        return  # Don't show section if no literature data

    st.markdown("### 📚 Referências da Literatura Científica")

    with st.expander("🔍 Ver resumos e referências bibliográficas", expanded=False):
        st.info("""
        Os valores apresentados nesta página foram validados com base em revisão sistemática
        da literatura científica peer-reviewed. Abaixo estão os resumos e referências para cada parâmetro.
        """)

        for item in literature_items:
            st.markdown(f"**{item['parameter']}**")
            st.write(f"📊 {item['summary']}")
            if item['references']:
                st.caption(f"📖 Referências: {item['references']}")
            st.markdown("---")


# ============================================================================
# MAIN RENDER
# ============================================================================

def main():
    """Main page render function - Database Integrated"""
    render_header()

    # Main navigation bar
    render_main_navigation(current_page="parametros")
    render_navigation_divider()

    # ========================================================================
    # SECTION 1: INDIVIDUAL RESIDUE SELECTION (NOW FIRST!)
    # ========================================================================

    # Selector returns full residue data dict
    residue_data = render_hierarchical_residue_selector()

    if not residue_data:
        st.info("👆 Selecione um setor e resíduo acima para visualizar os dados detalhados")

        # Show overview charts when no residue is selected
        st.markdown("---")
        st.markdown("### 📊 Visão Geral do Banco de Dados")

        # BMP Comparison Chart (ALL RESIDUES)
        st.markdown("#### 📊 Comparação de BMP - Todos os Resíduos")

        st.info("""
        **Visualização completa do banco de dados:** Todos os 38 resíduos catalogados com BMP validado.
        Cores indicam o setor: 🌾 Agricultura (verde), 🐄 Pecuária (laranja), 🏙️ Urbano (roxo), 🏭 Industrial (azul)
        """)

        try:
            df_all = get_all_residues_with_params()
            fig_bmp = create_bmp_comparison_bar(df_all)
            st.plotly_chart(fig_bmp, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao carregar gráfico de comparação: {e}")

        st.markdown("---")

        # Parameter Box Plots by Sector
        st.markdown("#### 📈 Distribuição de Parâmetros por Setor")

        col1, col2, col3 = st.columns(3)

        try:
            df_all = get_all_residues_with_params()

            with col1:
                fig_bmp_box = create_parameter_boxplot(df_all, 'bmp', 'BMP', 'mL CH₄/g VS')
                st.plotly_chart(fig_bmp_box, use_container_width=True)

            with col2:
                fig_ts_box = create_parameter_boxplot(df_all, 'ts', 'Sólidos Totais', '%')
                st.plotly_chart(fig_ts_box, use_container_width=True)

            with col3:
                fig_vs_box = create_parameter_boxplot(df_all, 'vs', 'Sólidos Voláteis', '%')
                st.plotly_chart(fig_vs_box, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao carregar box plots: {e}")

        # Show instructions
        st.markdown("---")
        st.markdown("### 📚 Sobre os Parâmetros Químicos")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            #### 🧬 Composição Química

            A composição química é fundamental para entender o potencial de produção de biogás de cada resíduo.

            **Parâmetros principais:**
            - **BMP** (Biochemical Methane Potential): Potencial metanogênico
            - **ST/SV** (Sólidos Totais/Voláteis): Conteúdo orgânico
            - **C:N** (Relação Carbono:Nitrogênio): Equilíbrio nutricional
            - **Nutrientes** (N, P, K): Composição do biofertilizante

            Os valores apresentados são baseados em **revisão sistemática da literatura científica**,
            com foco em estudos brasileiros e contexto tropical.
            """)

        with col2:
            st.markdown("""
            #### 🗄️ Banco de Dados Integrado

            Esta página agora carrega dados diretamente do banco de dados validado:

            **Estatísticas:**
            - **38 resíduos** catalogados e validados
            - **100% completude** - todos os resíduos têm BMP > 0
            - **4 setores** (Agricultura, Pecuária, Urbano, Industrial)
            - **Ranges validados** (mín/médio/máx) da literatura

            **📊 Ranges MIN/MEAN/MAX:**
            Os ranges mostram a variabilidade encontrada na literatura, permitindo
            entender a robustez do processo e adaptar para condições locais.
            """)

        return

    st.markdown("---")

    # Data already loaded by selector - no need to load again!
    # residue_data is already a dict with all fields from database

    # Display residue info
    st.markdown(f"## {residue_data.get('nome', 'N/A')}")

    sector_names = {
        'AG_AGRICULTURA': '🌾 Agricultura',
        'PC_PECUARIA': '🐄 Pecuária',
        'UR_URBANO': '🏙️ Urbano',
        'IN_INDUSTRIAL': '🏭 Industrial'
    }

    st.markdown(f"**Setor:** {sector_names.get(residue_data.get('setor', ''), 'N/A')}")

    st.markdown("---")

    # Load all residues data for sector comparisons
    try:
        df_all = get_all_residues_with_params()
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        df_all = pd.DataFrame()

    # Render all sections
    render_chemical_parameters_from_db(residue_data)

    st.markdown("---")

    # Enhanced metrics cards with sector comparison
    if not df_all.empty:
        render_enhanced_metrics(residue_data, df_all)
        st.markdown("---")

    # Radar chart - multi-dimensional comparison
    if not df_all.empty:
        render_radar_chart(residue_data, df_all)
        st.markdown("---")

    # Sector comparison bars
    if not df_all.empty:
        render_sector_comparison_bars(residue_data, df_all)
        st.markdown("---")

    # Literature references section
    render_literature_references(residue_data)

    st.markdown("---")

    # Link to lab comparison tool
    st.markdown("### 🔬 Próximo Passo: Validação Laboratorial")

    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        if st.button("🔬 Ir para Comparação Laboratorial", use_container_width=True, type="primary"):
            st.switch_page("pages/4_🔬_Comparacao_Laboratorial.py")

    st.info("💡 **Dica:** Use a ferramenta de comparação laboratorial para validar seus dados experimentais com os valores de referência apresentados acima!")

    # Cache management footer
    st.markdown("---")
    with st.expander("🔧 Gerenciamento de Cache (Debug)"):
        st.caption("""
        **Cache Info:** Os dados são armazenados em cache por 1 hora para melhor performance.
        Se você atualizou o banco de dados e não vê as mudanças, clique no botão abaixo ou pressione 'C' no teclado.
        """)

        col1, col2 = st.columns([3, 1])

        with col1:
            from datetime import datetime
            st.caption(f"📅 Última atualização desta página: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        with col2:
            if st.button("🔄 Limpar Cache", type="secondary", use_container_width=True):
                from src.data_handler import clear_all_caches
                clear_all_caches()
                st.success("✅ Cache limpo! Atualize a página (F5).")
                st.rerun()


if __name__ == "__main__":
    main()
