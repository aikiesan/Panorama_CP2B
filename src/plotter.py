"""
Plotter Module - Single Responsibility Principle
Handles all visualization creation using Plotly.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from src import plotly_theme as theme


# Color scheme for biogas theme (green palette)
COLORS = {
    'primary': '#2ecc71',      # Green
    'secondary': '#27ae60',    # Dark green
    'tertiary': '#16a085',     # Teal
    'agricultura': '#27ae60',  # Dark green
    'pecuaria': '#e67e22',     # Orange
    'urbano': '#3498db',       # Blue
    'background': '#ecf0f1',   # Light gray
}

SECTOR_COLORS = {
    'Agricultura': COLORS['agricultura'],
    'Pecuária': COLORS['pecuaria'],
    'Urbano': COLORS['urbano']
}


def criar_mapa_coropleth_sp(df: pd.DataFrame, geojson_path: str) -> go.Figure:
    """
    Creates an interactive choropleth map of São Paulo municipalities.
    
    Args:
        df: Municipality DataFrame with columns ['codigo_municipio', 'total_final_m_ano']
        geojson_path: Path to GeoJSON file with municipality boundaries
        
    Returns:
        go.Figure: Plotly choropleth map
    """
    # Load GeoJSON
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson = json.load(f)
    
    # Prepare data - convert codigo_municipio to string for matching
    df_map = df.copy()
    df_map['codigo_municipio_str'] = df_map['codigo_municipio'].astype(str)
    
    # Create choropleth map
    fig = px.choropleth_mapbox(
        df_map,
        geojson=geojson,
        featureidkey="properties.CD_MUN",
        locations='codigo_municipio_str',
        color='total_final_m_ano',
        hover_name='nome_municipio',
        hover_data={
            'total_final_m_ano': ':,.0f',
            'total_agricola_m_ano': ':,.0f',
            'total_pecuaria_m_ano': ':,.0f',
            'total_urbano_m_ano': ':,.0f',
            'codigo_municipio_str': False
        },
        color_continuous_scale='Greens',
        mapbox_style="carto-positron",
        center={"lat": -22.5, "lon": -48.5},
        zoom=5.5,
        opacity=0.7,
        labels={
            'total_final_m_ano': 'Potencial Total (m³/ano)',
            'total_agricola_m_ano': 'Agricultura (m³/ano)',
            'total_pecuaria_m_ano': 'Pecuária (m³/ano)',
            'total_urbano_m_ano': 'Urbano (m³/ano)'
        }
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        title={
            'text': 'Potencial de Biogás por Município',
            'x': 0.5,
            'xanchor': 'center'
        },
        height=500
    )
    
    return fig


def criar_grafico_donut_setor(df_setor: pd.DataFrame) -> go.Figure:
    """
    Creates a donut chart showing biogas distribution by sector.

    Args:
        df_setor: DataFrame with columns ['setor', 'volume']

    Returns:
        go.Figure: Plotly donut chart
    """
    colors = [SECTOR_COLORS.get(setor, COLORS['primary']) for setor in df_setor['setor']]

    fig = px.pie(
        df_setor,
        names='setor',
        values='volume',
        hole=0.5,
        color='setor',
        color_discrete_map=SECTOR_COLORS
    )

    fig.update_traces(
        textinfo='percent+label',
        textfont_size=14,
        marker=dict(line=dict(color='white', width=2))
    )

    # Apply custom layout
    layout = theme.get_custom_layout(title='Distribuição por Setor', height=400, show_legend=True)
    layout['legend'] = dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        font=dict(family='Inter, sans-serif', size=12, color=theme.COLORS['text_primary'])
    )
    layout['margin'] = dict(t=50, b=20, l=20, r=120)

    fig.update_layout(**layout)

    return fig


def criar_grafico_barras_substrato(df_substrato: pd.DataFrame) -> go.Figure:
    """
    Creates a horizontal bar chart for substrate breakdown.
    
    Args:
        df_substrato: DataFrame with columns ['substrato', 'volume']
        
    Returns:
        go.Figure: Plotly bar chart
    """
    # Sort by volume for better visualization
    df_plot = df_substrato.sort_values('volume', ascending=True)
    
    fig = px.bar(
        df_plot,
        x='volume',
        y='substrato',
        orientation='h',
        color='volume',
        color_continuous_scale='Greens',
        labels={'volume': 'Potencial (m³/ano)', 'substrato': 'Substrato'}
    )
    
    fig.update_traces(
        texttemplate='%{x:,.0f}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Potencial: %{x:,.0f} m³/ano<extra></extra>'
    )
    
    # Apply custom layout
    layout = theme.get_custom_layout(title='Potencial de Biogás por Substrato', height=max(400, len(df_plot) * 40), show_legend=False)
    layout['xaxis']['title']['text'] = 'Potencial (m³/ano)'
    layout['yaxis']['title']['text'] = ''
    layout['margin'] = dict(l=150, r=100, t=50, b=50)

    fig.update_layout(**layout)

    return fig


def criar_grafico_top_municipios(df_top: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Creates a stacked bar chart of top municipalities by biogas potential.
    
    Args:
        df_top: DataFrame with top municipalities and sector breakdowns
        top_n: Number of municipalities to display
        
    Returns:
        go.Figure: Plotly stacked bar chart
    """
    # Prepare data
    df_plot = df_top.head(top_n).copy()
    df_plot = df_plot.sort_values('total_final_m_ano', ascending=True)
    
    fig = go.Figure()
    
    # Add traces for each sector
    fig.add_trace(go.Bar(
        name='Agricultura',
        y=df_plot['nome_municipio'],
        x=df_plot['total_agricola_m_ano'],
        orientation='h',
        marker=dict(color=COLORS['agricultura']),
        hovertemplate='<b>%{y}</b><br>Agricultura: %{x:,.0f} m³/ano<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Pecuária',
        y=df_plot['nome_municipio'],
        x=df_plot['total_pecuaria_m_ano'],
        orientation='h',
        marker=dict(color=COLORS['pecuaria']),
        hovertemplate='<b>%{y}</b><br>Pecuária: %{x:,.0f} m³/ano<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Urbano',
        y=df_plot['nome_municipio'],
        x=df_plot['total_urbano_m_ano'],
        orientation='h',
        marker=dict(color=COLORS['urbano']),
        hovertemplate='<b>%{y}</b><br>Urbano: %{x:,.0f} m³/ano<extra></extra>'
    ))
    
    # Apply custom layout
    layout = theme.get_custom_layout(title=f'Top {top_n} Municípios por Potencial de Biogás', height=max(400, top_n * 40), show_legend=True)
    layout['barmode'] = 'stack'
    layout['xaxis']['title']['text'] = 'Potencial (m³/ano)'
    layout['yaxis']['title']['text'] = ''
    layout['legend'] = dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(family='Inter, sans-serif', size=12, color=theme.COLORS['text_primary'])
    )
    layout['margin'] = dict(l=150, r=50, t=80, b=50)

    fig.update_layout(**layout)

    return fig


def criar_grafico_dispersao(df: pd.DataFrame, x_col: str, y_col: str, 
                            labels: dict = None) -> go.Figure:
    """
    Creates a scatter plot for exploring relationships between variables.
    
    Args:
        df: Municipality DataFrame
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        labels: Dictionary mapping column names to display labels
        
    Returns:
        go.Figure: Plotly scatter plot
    """
    if labels is None:
        labels = {x_col: x_col, y_col: y_col}
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        hover_name='nome_municipio',
        color='total_final_m_ano',
        size='total_final_m_ano',
        color_continuous_scale='Greens',
        labels=labels
    )
    
    fig.update_layout(
        title={
            'text': f'{labels.get(y_col, y_col)} vs {labels.get(x_col, x_col)}',
            'x': 0.5,
            'xanchor': 'center'
        },
        height=500
    )
    
    return fig


def criar_grafico_evolucao_categoria(df: pd.DataFrame) -> go.Figure:
    """
    Creates a bar chart showing distribution by potential category.
    
    Args:
        df: Municipality DataFrame with 'categoria_potencial' column
        
    Returns:
        go.Figure: Plotly bar chart
    """
    # Count municipalities by category
    categoria_counts = df['categoria_potencial'].value_counts().reset_index()
    categoria_counts.columns = ['categoria', 'quantidade']
    
    # Define category order
    category_order = ['BAIXO', 'MÉDIO', 'ALTO']
    categoria_counts['categoria'] = pd.Categorical(
        categoria_counts['categoria'], 
        categories=category_order, 
        ordered=True
    )
    categoria_counts = categoria_counts.sort_values('categoria')
    
    fig = px.bar(
        categoria_counts,
        x='categoria',
        y='quantidade',
        color='categoria',
        color_discrete_sequence=['#e74c3c', '#f39c12', '#27ae60'],
        labels={'categoria': 'Categoria de Potencial', 'quantidade': 'Número de Municípios'}
    )
    
    fig.update_traces(
        texttemplate='%{y}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Municípios: %{y}<extra></extra>'
    )
    
    fig.update_layout(
        title={
            'text': 'Distribuição de Municípios por Categoria de Potencial',
            'x': 0.5,
            'xanchor': 'center'
        },
        showlegend=False,
        height=400,
        xaxis_title='Categoria de Potencial',
        yaxis_title='Número de Municípios'
    )
    
    return fig


def criar_grafico_radar_municipio(mun_data: pd.Series) -> go.Figure:
    """
    Creates a radar chart showing all substrate contributions for a municipality.
    
    Args:
        mun_data: Series with municipality data
        
    Returns:
        go.Figure: Plotly radar chart
    """
    # Extract substrate values
    substratos = {
        'Cana': mun_data.get('biogas_cana_m_ano', 0),
        'Soja': mun_data.get('biogas_soja_m_ano', 0),
        'Milho': mun_data.get('biogas_milho_m_ano', 0),
        'Bovinos': mun_data.get('biogas_bovinos_m_ano', 0),
        'Suínos': mun_data.get('biogas_suino_m_ano', 0),
        'Aves': mun_data.get('biogas_aves_m_ano', 0),
        'RSU': mun_data.get('rsu_potencial_m_ano', 0),
        'Silvicultura': mun_data.get('biogas_silvicultura_m_ano', 0)
    }
    
    # Filter out zero values and normalize
    substratos_filtrados = {k: v for k, v in substratos.items() if v > 0}
    
    if not substratos_filtrados:
        # Return empty figure if no data
        fig = go.Figure()
        fig.add_annotation(
            text="Sem dados disponíveis",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20)
        )
        return fig
    
    categories = list(substratos_filtrados.keys())
    values = list(substratos_filtrados.values())
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor=COLORS['primary'],
        opacity=0.6,
        line=dict(color=COLORS['secondary'], width=2),
        hovertemplate='<b>%{theta}</b><br>%{r:,.0f} m³/ano<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                showticklabels=True
            )
        ),
        title={
            'text': f'Composição do Potencial - {mun_data.get("nome_municipio", "Município")}',
            'x': 0.5,
            'xanchor': 'center'
        },
        height=500
    )
    
    return fig

