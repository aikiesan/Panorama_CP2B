"""
Custom Plotly Theme for Agricultural Residue Biogas Explorer
Matches the premium UI/UX design system
"""

import plotly.graph_objects as go
import plotly.express as px

# Design System Colors
COLORS = {
    # Primary
    'teal': '#2EC4B6',
    'cyan': '#00D9FF',
    'green': '#5CB85C',
    'red': '#FF6B6B',
    
    # Text
    'text_primary': '#0F1A2A',
    'text_secondary': '#64748B',
    
    # Backgrounds
    'bg_primary': '#FFFFFF',
    'bg_secondary': '#F5F7FA',
    'bg_card': '#FAFBFC',
    
    # Borders
    'border_light': '#E2E8F0',
    'border_medium': '#CBD5E1',
}

# Color Scales
SEQUENTIAL_GREEN = [
    '#d4edda', '#b7e4c7', '#95d5b2', '#74c69d',
    '#52b788', '#40916c', '#2d6a4f', '#1e7e34'
]

DIVERGING_RWG = [
    '#FF6B6B', '#FFA07A', '#FFD4B2', '#FFFFFF',
    '#D4EDDA', '#95D5B2', '#52B788', '#1E7E34'
]

CATEGORICAL = ['#2EC4B6', '#00D9FF', '#5CB85C', '#0F1A2A', '#64748B']


def get_custom_layout(title="", height=500, show_legend=True):
    """
    Returns a custom Plotly layout following the design system.
    
    Args:
        title: Chart title
        height: Chart height in pixels
        show_legend: Whether to show legend
        
    Returns:
        dict: Plotly layout configuration
    """
    return {
        'title': {
            'text': title,
            'font': {
                'family': 'Inter, sans-serif',
                'size': 20,
                'color': COLORS['text_primary'],
                'weight': 600
            },
            'x': 0.5,
            'xanchor': 'center'
        },
        'font': {
            'family': 'Inter, sans-serif',
            'size': 14,
            'color': COLORS['text_primary']
        },
        'paper_bgcolor': COLORS['bg_primary'],
        'plot_bgcolor': COLORS['bg_primary'],
        'height': height,
        'showlegend': show_legend,
        'legend': {
            'font': {
                'family': 'Inter, sans-serif',
                'size': 12,
                'color': COLORS['text_secondary']
            },
            'bgcolor': 'rgba(255, 255, 255, 0.9)',
            'bordercolor': COLORS['border_light'],
            'borderwidth': 1
        },
        'margin': {'l': 60, 'r': 40, 't': 80, 'b': 60},
        'xaxis': {
            'gridcolor': COLORS['border_light'],
            'linecolor': COLORS['border_medium'],
            'title': {
                'font': {
                    'family': 'Inter, sans-serif',
                    'size': 14,
                    'color': COLORS['text_secondary']
                }
            },
            'tickfont': {
                'family': 'Inter, sans-serif',
                'size': 12,
                'color': COLORS['text_secondary']
            }
        },
        'yaxis': {
            'gridcolor': COLORS['border_light'],
            'linecolor': COLORS['border_medium'],
            'title': {
                'font': {
                    'family': 'Inter, sans-serif',
                    'size': 14,
                    'color': COLORS['text_secondary']
                }
            },
            'tickfont': {
                'family': 'Inter, sans-serif',
                'size': 12,
                'color': COLORS['text_secondary']
            }
        },
        'hovermode': 'closest',
        'hoverlabel': {
            'bgcolor': COLORS['text_primary'],
            'bordercolor': COLORS['text_primary'],
            'font': {
                'family': 'Inter, sans-serif',
                'size': 13,
                'color': '#FFFFFF'
            }
        }
    }


def create_donut_chart(values, labels, title="", colors=None):
    """
    Creates a professional donut chart for composition data.
    
    Args:
        values: List of values
        labels: List of labels
        title: Chart title
        colors: Custom color list (uses teal scale if None)
        
    Returns:
        go.Figure: Plotly figure object
    """
    if colors is None:
        colors = SEQUENTIAL_GREEN[:len(values)]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(
            colors=colors,
            line=dict(color=COLORS['bg_primary'], width=2)
        ),
        textfont=dict(
            family='Inter, sans-serif',
            size=14,
            color=COLORS['text_primary']
        ),
        hovertemplate='<b>%{label}</b><br>%{value}<br>%{percent}<extra></extra>'
    )])
    
    layout = get_custom_layout(title=title, height=400, show_legend=True)
    layout['annotations'] = [{
        'text': f'<b>Total</b><br>{sum(values):.1f}',
        'x': 0.5,
        'y': 0.5,
        'font': {
            'family': 'Inter, sans-serif',
            'size': 16,
            'color': COLORS['text_primary']
        },
        'showarrow': False
    }]
    
    fig.update_layout(**layout)
    
    return fig


def create_radar_chart(categories, values, title="", name=""):
    """
    Creates a radar chart for chemical composition profile.
    
    Args:
        categories: List of category names
        values: List of values
        title: Chart title
        name: Trace name
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor=f'rgba(46, 196, 182, 0.2)',
        line=dict(color=COLORS['teal'], width=2),
        marker=dict(size=8, color=COLORS['teal']),
        name=name,
        hovertemplate='<b>%{theta}</b><br>%{r:.2f}<extra></extra>'
    ))
    
    layout = get_custom_layout(title=title, height=500, show_legend=False)
    layout['polar'] = {
        'radialaxis': {
            'visible': True,
            'gridcolor': COLORS['border_light'],
            'linecolor': COLORS['border_medium'],
            'tickfont': {
                'family': 'Inter, sans-serif',
                'size': 11,
                'color': COLORS['text_secondary']
            }
        },
        'angularaxis': {
            'gridcolor': COLORS['border_light'],
            'linecolor': COLORS['border_medium'],
            'tickfont': {
                'family': 'Inter, sans-serif',
                'size': 12,
                'color': COLORS['text_primary']
            }
        },
        'bgcolor': COLORS['bg_primary']
    }
    
    fig.update_layout(**layout)
    
    return fig


def create_bar_chart(x, y, title="", x_label="", y_label="", orientation='v', color=None):
    """
    Creates a professional bar chart.
    
    Args:
        x: X-axis data
        y: Y-axis data
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        orientation: 'v' for vertical, 'h' for horizontal
        color: Bar color (uses teal if None)
        
    Returns:
        go.Figure: Plotly figure object
    """
    if color is None:
        color = COLORS['teal']
    
    if orientation == 'h':
        fig = go.Figure(data=[go.Bar(
            x=y,
            y=x,
            orientation='h',
            marker=dict(
                color=color,
                line=dict(color=COLORS['border_light'], width=1)
            ),
            hovertemplate='<b>%{y}</b><br>%{x:.2f}<extra></extra>'
        )])
    else:
        fig = go.Figure(data=[go.Bar(
            x=x,
            y=y,
            marker=dict(
                color=color,
                line=dict(color=COLORS['border_light'], width=1)
            ),
            hovertemplate='<b>%{x}</b><br>%{y:.2f}<extra></extra>'
        )])
    
    layout = get_custom_layout(title=title, height=400, show_legend=False)
    if x_label:
        layout['xaxis']['title']['text'] = x_label
    if y_label:
        layout['yaxis']['title']['text'] = y_label
    
    fig.update_layout(**layout)
    
    return fig


def create_box_plot(data, labels, title="", y_label=""):
    """
    Creates a box plot showing literature ranges.
    
    Args:
        data: List of lists containing data points for each box
        labels: List of labels for each box
        title: Chart title
        y_label: Y-axis label
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure()
    
    for i, (d, label) in enumerate(zip(data, labels)):
        fig.add_trace(go.Box(
            y=d,
            name=label,
            marker=dict(color=CATEGORICAL[i % len(CATEGORICAL)]),
            boxmean='sd',  # Show mean and standard deviation
            hovertemplate='<b>%{fullData.name}</b><br>Value: %{y:.2f}<extra></extra>'
        ))
    
    layout = get_custom_layout(title=title, height=450, show_legend=True)
    if y_label:
        layout['yaxis']['title']['text'] = y_label
    layout['showlegend'] = len(labels) > 1
    
    fig.update_layout(**layout)
    
    return fig


def create_metric_comparison_chart(categories, values1, values2, label1="", label2="", title="", x_label="", y_label=""):
    """
    Creates a grouped bar chart for comparing metrics.
    
    Args:
        categories: List of category names
        values1: First set of values
        values2: Second set of values
        label1: Label for first dataset
        label2: Label for second dataset
        title: Chart title
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name=label1,
        x=categories,
        y=values1,
        marker=dict(color=COLORS['teal']),
        hovertemplate='<b>%{x}</b><br>' + label1 + ': %{y:.2f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name=label2,
        x=categories,
        y=values2,
        marker=dict(color=COLORS['cyan']),
        hovertemplate='<b>%{x}</b><br>' + label2 + ': %{y:.2f}<extra></extra>'
    ))
    
    layout = get_custom_layout(title=title, height=450, show_legend=True)
    layout['barmode'] = 'group'
    if x_label:
        layout['xaxis']['title']['text'] = x_label
    if y_label:
        layout['yaxis']['title']['text'] = y_label
    
    fig.update_layout(**layout)
    
    return fig


def create_scatter_plot(x, y, labels=None, title="", x_label="", y_label="", size=None, color=None):
    """
    Creates a professional scatter plot.
    
    Args:
        x: X-axis data
        y: Y-axis data
        labels: Point labels for hover
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        size: Point sizes (optional)
        color: Point colors or color scale (optional)
        
    Returns:
        go.Figure: Plotly figure object
    """
    if size is None:
        size = 8
    
    marker_config = dict(
        size=size if isinstance(size, int) else size,
        line=dict(width=1, color=COLORS['border_light'])
    )
    
    if color is not None:
        if isinstance(color, str):
            marker_config['color'] = color
        else:
            marker_config['color'] = color
            marker_config['colorscale'] = SEQUENTIAL_GREEN
            marker_config['showscale'] = True
    else:
        marker_config['color'] = COLORS['teal']
    
    hover_text = labels if labels is not None else [f"Point {i+1}" for i in range(len(x))]
    
    fig = go.Figure(data=[go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=marker_config,
        text=hover_text,
        hovertemplate='<b>%{text}</b><br>' + x_label + ': %{x:.2f}<br>' + y_label + ': %{y:.2f}<extra></extra>'
    )])
    
    layout = get_custom_layout(title=title, height=500, show_legend=False)
    if x_label:
        layout['xaxis']['title']['text'] = x_label
    if y_label:
        layout['yaxis']['title']['text'] = y_label
    
    fig.update_layout(**layout)
    
    return fig


def apply_theme_to_figure(fig):
    """
    Applies the custom theme to an existing Plotly figure.
    
    Args:
        fig: Plotly figure object
        
    Returns:
        go.Figure: Updated figure
    """
    layout = get_custom_layout()
    fig.update_layout(**layout)
    return fig

