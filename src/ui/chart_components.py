"""
Chart Components - Advanced Visualizations for CP2B Dashboard
Single Responsibility: Reusable Plotly chart generation functions

Provides 7 new chart types:
1. Waterfall Chart - SAF factor breakdown
2. Box Plots - Parameter ranges by sector
3. Violin Plots - Distribution analysis
4. Radar Charts - Multi-parameter sector comparison
5. Correlation Matrix - Heatmap for parameters
6. Heatmap - Geographic/sector analysis
7. 3D Scatter - Multi-dimensional relationships
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict, Optional


# ============================================================================
# COLOR SCHEMES - Standardized across all charts
# ============================================================================

SECTOR_COLORS = {
    'AG_AGRICULTURA': '#10b981',  # Green
    'PC_PECUARIA': '#f59e0b',      # Orange
    'UR_URBANO': '#8b5cf6',        # Purple
    'IN_INDUSTRIAL': '#3b82f6'     # Blue
}

SECTOR_NAMES = {
    'AG_AGRICULTURA': 'Agricultura',
    'PC_PECUARIA': 'Pecuária',
    'UR_URBANO': 'Urbano',
    'IN_INDUSTRIAL': 'Industrial'
}


def get_sector_color(sector_code: str) -> str:
    """Get color for sector code"""
    return SECTOR_COLORS.get(sector_code, '#6b7280')


def get_sector_name(sector_code: str) -> str:
    """Get friendly name for sector code"""
    return SECTOR_NAMES.get(sector_code, sector_code)


# ============================================================================
# 1. WATERFALL CHART - SAF Factor Breakdown
# ============================================================================

def create_waterfall_chart(
    fc: float,
    fcp: float,
    fs: float,
    fl: float,
    residue_name: str = "Resíduo"
) -> go.Figure:
    """
    Create waterfall chart showing SAF factor breakdown.

    Shows progressive impact: 100% → FC → FCp → FS → FL → Final

    IMPORTANT: FCp = % AVAILABLE (not % competing)
    Formula: SAF = FC × FCp × FS × FL × 100%

    Args:
        fc: Collection factor (0-1) - Collection efficiency
        fcp: Competition factor (0-1) - % AVAILABLE after competing uses
        fs: Seasonality factor (0-1) - Seasonal availability
        fl: Logistic factor (0-1) - Logistic viability
        residue_name: Name of residue for title

    Returns:
        go.Figure: Waterfall chart
    """
    # Calculate step-by-step values (multiplicative, not subtractive)
    initial = 100.0
    after_fc = initial * fc
    after_fcp = after_fc * fcp  # Changed: FCp multiplies (it's % available)
    after_fs = after_fcp * fs
    final = after_fs * fl

    # Calculate deltas
    delta_fc = after_fc - initial
    delta_fcp = after_fcp - after_fc
    delta_fs = after_fs - after_fcp
    delta_fl = final - after_fs

    # Label showing what FCp means
    fcp_label = f"FCp ({fcp:.0%} disp.)"  # "disp." = disponível after competition

    fig = go.Figure(go.Waterfall(
        name="SAF Breakdown",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "relative", "total"],
        x=["Teórico (100%)", f"FC ({fc:.0%})", fcp_label, f"FS ({fs:.0%})", f"FL ({fl:.0%})", "Final"],
        y=[initial, delta_fc, delta_fcp, delta_fs, delta_fl, final],
        text=[f"{initial:.1f}%", f"{delta_fc:+.1f}%", f"{delta_fcp:+.1f}%",
              f"{delta_fs:+.1f}%", f"{delta_fl:+.1f}%", f"{final:.1f}%"],
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "#ef4444"}},
        increasing={"marker": {"color": "#10b981"}},
        totals={"marker": {"color": "#3b82f6"}}
    ))

    fig.update_layout(
        title=f"Breakdown de Disponibilidade (SAF) - {residue_name}",
        showlegend=False,
        height=400,
        xaxis_title="Fator",
        yaxis_title="Disponibilidade (%)",
        yaxis=dict(range=[0, 110])
    )

    return fig


# ============================================================================
# 2. BOX PLOTS - Parameter Ranges by Sector
# ============================================================================

def create_parameter_boxplot(
    df: pd.DataFrame,
    parameter: str,
    parameter_label: str,
    unit: str = ""
) -> go.Figure:
    """
    Create box plot showing parameter distribution by sector.

    Args:
        df: DataFrame with columns [setor, {parameter}_min, {parameter}_medio, {parameter}_max]
        parameter: Parameter name (e.g., 'bmp', 'ts', 'vs')
        parameter_label: Display label (e.g., 'BMP', 'Sólidos Totais')
        unit: Unit of measurement

    Returns:
        go.Figure: Box plot
    """
    fig = go.Figure()

    for sector_code in ['AG_AGRICULTURA', 'PC_PECUARIA', 'UR_URBANO', 'IN_INDUSTRIAL']:
        sector_data = df[df['setor'] == sector_code]

        if sector_data.empty:
            continue

        # Get min, mean, max values
        min_col = f"{parameter}_min"
        mean_col = f"{parameter}_medio"
        max_col = f"{parameter}_max"

        if mean_col not in df.columns:
            continue

        values = []
        for _, row in sector_data.iterrows():
            # Add min, mean, max for each residue to create distribution
            if pd.notna(row.get(min_col)):
                values.append(row[min_col])
            if pd.notna(row.get(mean_col)):
                values.append(row[mean_col])
            if pd.notna(row.get(max_col)):
                values.append(row[max_col])

        if not values:
            continue

        fig.add_trace(go.Box(
            y=values,
            name=get_sector_name(sector_code),
            marker_color=get_sector_color(sector_code),
            boxmean='sd'  # Show mean and standard deviation
        ))

    unit_str = f" ({unit})" if unit else ""
    fig.update_layout(
        title=f"Distribuição de {parameter_label} por Setor{unit_str}",
        yaxis_title=f"{parameter_label}{unit_str}",
        xaxis_title="Setor",
        showlegend=True,
        height=450
    )

    return fig


# ============================================================================
# 3. VIOLIN PLOTS - Distribution Analysis
# ============================================================================

def create_violin_plot(
    df: pd.DataFrame,
    parameter: str,
    parameter_label: str,
    unit: str = ""
) -> go.Figure:
    """
    Create violin plot showing parameter distribution by sector.

    More detailed than box plot - shows full distribution shape.

    Args:
        df: DataFrame with columns [setor, nome, {parameter}_medio]
        parameter: Parameter name
        parameter_label: Display label
        unit: Unit of measurement

    Returns:
        go.Figure: Violin plot
    """
    fig = go.Figure()

    param_col = f"{parameter}_medio"
    if param_col not in df.columns:
        return fig

    for sector_code in ['AG_AGRICULTURA', 'PC_PECUARIA', 'UR_URBANO', 'IN_INDUSTRIAL']:
        sector_data = df[df['setor'] == sector_code]

        if sector_data.empty:
            continue

        values = sector_data[param_col].dropna()

        if len(values) == 0:
            continue

        fig.add_trace(go.Violin(
            y=values,
            name=get_sector_name(sector_code),
            box_visible=True,
            meanline_visible=True,
            marker_color=get_sector_color(sector_code),
            line_color=get_sector_color(sector_code),
            fillcolor=get_sector_color(sector_code),
            opacity=0.6
        ))

    unit_str = f" ({unit})" if unit else ""
    fig.update_layout(
        title=f"Distribuição de {parameter_label} por Setor{unit_str}",
        yaxis_title=f"{parameter_label}{unit_str}",
        xaxis_title="Setor",
        showlegend=True,
        height=450
    )

    return fig


# ============================================================================
# 4. RADAR CHART - Multi-parameter Sector Comparison
# ============================================================================

def create_radar_chart(
    sector_data: Dict[str, Dict[str, float]],
    parameters: List[str],
    parameter_labels: List[str]
) -> go.Figure:
    """
    Create radar chart comparing multiple parameters across sectors.

    Args:
        sector_data: {sector_code: {param: value}}
        parameters: List of parameter names
        parameter_labels: List of display labels for parameters

    Returns:
        go.Figure: Radar chart
    """
    fig = go.Figure()

    for sector_code, data in sector_data.items():
        values = [data.get(param, 0) for param in parameters]

        # Close the polygon
        values.append(values[0])
        labels = parameter_labels + [parameter_labels[0]]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name=get_sector_name(sector_code),
            marker_color=get_sector_color(sector_code),
            line=dict(color=get_sector_color(sector_code))
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Comparação Multi-Parâmetros por Setor",
        height=500
    )

    return fig


# ============================================================================
# 5. CORRELATION MATRIX - Heatmap
# ============================================================================

def create_correlation_matrix(
    df: pd.DataFrame,
    parameters: List[str],
    parameter_labels: List[str]
) -> go.Figure:
    """
    Create correlation heatmap for multiple parameters.

    Args:
        df: DataFrame with parameter columns
        parameters: List of parameter column names
        parameter_labels: List of display labels

    Returns:
        go.Figure: Correlation heatmap
    """
    # Calculate correlation matrix
    corr_data = df[parameters].corr()

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_data.values,
        x=parameter_labels,
        y=parameter_labels,
        colorscale='RdBu',
        zmid=0,
        text=corr_data.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlação")
    ))

    fig.update_layout(
        title="Matriz de Correlação - Parâmetros Químicos",
        height=500,
        xaxis=dict(side='bottom'),
        yaxis=dict(side='left')
    )

    return fig


# ============================================================================
# 6. HEATMAP - Geographic/Sector Analysis
# ============================================================================

def create_sector_heatmap(
    df: pd.DataFrame,
    value_column: str,
    row_labels: List[str],
    col_labels: List[str],
    title: str = "Heatmap"
) -> go.Figure:
    """
    Create generic heatmap for geographic or sector analysis.

    Args:
        df: DataFrame with data
        value_column: Column containing values
        row_labels: Labels for rows
        col_labels: Labels for columns
        title: Chart title

    Returns:
        go.Figure: Heatmap
    """
    # Pivot data for heatmap
    if 'setor' in df.columns and 'nome' in df.columns:
        pivot = df.pivot_table(
            index='setor',
            columns='nome',
            values=value_column,
            aggfunc='mean'
        )

        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=[get_sector_name(s) for s in pivot.index],
            colorscale='Viridis',
            colorbar=dict(title=value_column)
        ))
    else:
        # Generic heatmap
        fig = go.Figure(data=go.Heatmap(
            z=df.values,
            x=col_labels,
            y=row_labels,
            colorscale='Viridis'
        ))

    fig.update_layout(
        title=title,
        height=500,
        xaxis=dict(side='bottom'),
        yaxis=dict(side='left')
    )

    return fig


# ============================================================================
# 7. 3D SCATTER - Multi-dimensional Relationships
# ============================================================================

def create_3d_scatter(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    z_col: str,
    x_label: str,
    y_label: str,
    z_label: str,
    color_col: str = 'setor',
    size_col: Optional[str] = None,
    hover_name: str = 'nome'
) -> go.Figure:
    """
    Create 3D scatter plot showing relationships between 3 parameters.

    Args:
        df: DataFrame with data
        x_col, y_col, z_col: Column names for x, y, z axes
        x_label, y_label, z_label: Axis labels
        color_col: Column for color grouping
        size_col: Optional column for marker size
        hover_name: Column for hover labels

    Returns:
        go.Figure: 3D scatter plot
    """
    # Prepare data
    df_clean = df.dropna(subset=[x_col, y_col, z_col])

    if df_clean.empty:
        return go.Figure()

    # Create color mapping for sectors
    df_clean['color'] = df_clean[color_col].map(get_sector_color)
    df_clean['sector_name'] = df_clean[color_col].map(get_sector_name)

    # Size scaling
    if size_col and size_col in df_clean.columns:
        sizes = df_clean[size_col]
        sizes_normalized = (sizes - sizes.min()) / (sizes.max() - sizes.min()) * 20 + 5
    else:
        sizes_normalized = [10] * len(df_clean)

    fig = go.Figure()

    # Add trace for each sector
    for sector_code in df_clean[color_col].unique():
        sector_df = df_clean[df_clean[color_col] == sector_code]

        fig.add_trace(go.Scatter3d(
            x=sector_df[x_col],
            y=sector_df[y_col],
            z=sector_df[z_col],
            mode='markers',
            name=get_sector_name(sector_code),
            marker=dict(
                size=sizes_normalized[:len(sector_df)] if isinstance(sizes_normalized, np.ndarray) else [10] * len(sector_df),
                color=get_sector_color(sector_code),
                opacity=0.8,
                line=dict(width=0.5, color='white')
            ),
            text=sector_df[hover_name] if hover_name in sector_df.columns else None,
            hovertemplate=f'<b>%{{text}}</b><br>{x_label}: %{{x}}<br>{y_label}: %{{y}}<br>{z_label}: %{{z}}<extra></extra>'
        ))

    fig.update_layout(
        title="Análise Tridimensional - Parâmetros",
        scene=dict(
            xaxis_title=x_label,
            yaxis_title=y_label,
            zaxis_title=z_label
        ),
        height=600,
        showlegend=True
    )

    return fig


# ============================================================================
# 8. BAR CHART - BMP Comparison Across All Residues
# ============================================================================

def create_bmp_comparison_bar(df: pd.DataFrame) -> go.Figure:
    """
    Create bar chart comparing BMP values across all residues, colored by sector.

    Args:
        df: DataFrame with columns [nome, bmp_medio, setor]

    Returns:
        go.Figure: Bar chart
    """
    # Sort by BMP value
    df_sorted = df.sort_values('bmp_medio', ascending=True)

    # Create color array based on sector
    colors = [get_sector_color(sector) for sector in df_sorted['setor']]

    fig = go.Figure(go.Bar(
        x=df_sorted['bmp_medio'],
        y=df_sorted['nome'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(width=0.5, color='white')
        ),
        text=df_sorted['bmp_medio'].round(3),
        texttemplate='%{text:.3f}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>BMP: %{x:.3f} m³/kg VS<extra></extra>'
    ))

    fig.update_layout(
        title="Comparação de BMP - Todos os Resíduos",
        xaxis_title="BMP (m³ CH₄/kg VS)",
        yaxis_title="Resíduo",
        height=max(400, len(df_sorted) * 20),  # Dynamic height based on number of residues
        showlegend=False,
        margin=dict(l=200)  # Left margin for long residue names
    )

    return fig


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_large_number(value: float, unit: str = "") -> str:
    """Format large numbers with K, M, B suffixes"""
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B {unit}"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M {unit}"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}K {unit}"
    else:
        return f"{value:.1f} {unit}"
