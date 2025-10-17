"""
Premium UI Components Module
Reusable Streamlit components following the design system
"""

import streamlit as st
import pandas as pd
from pathlib import Path


def load_css():
    """
    Loads and applies the custom CSS theme.
    Should be called at the start of the app.
    """
    css_file = Path(__file__).parent.parent / "assets" / "styles.css"
    
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning("Custom CSS file not found. Using default Streamlit theme.")


def render_hero_section(title, subtitle, show_selectors=True):
    """
    Renders the hero section with gradient background and query interface.
    
    Args:
        title: Main title text
        subtitle: Subtitle/description text
        show_selectors: Whether to show the crop/residue selectors
        
    Returns:
        dict: Selected values from dropdowns (if show_selectors=True)
    """
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if show_selectors:
        # Selector interface
        st.markdown("<div style='margin-top: -12px;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            crop = st.selectbox(
                "Select Crop",
                ["Sugarcane", "Corn", "Soybean", "Rice", "Wheat", "Coffee"],
                key="hero_crop_selector"
            )
        
        with col2:
            residue_types = {
                "Sugarcane": ["Bagasse", "Straw", "Filter Cake"],
                "Corn": ["Stover", "Cob", "Husk"],
                "Soybean": ["Straw", "Hulls"],
                "Rice": ["Straw", "Husk"],
                "Wheat": ["Straw", "Bran"],
                "Coffee": ["Pulp", "Husk", "Parchment"]
            }
            residue = st.selectbox(
                "Residue Type",
                residue_types.get(crop, ["All"]),
                key="hero_residue_selector"
            )
        
        with col3:
            region = st.selectbox(
                "Region",
                ["São Paulo", "Brazil", "Global", "Latin America"],
                key="hero_region_selector"
            )
        
        return {"crop": crop, "residue": residue, "region": region}
    
    return {}


def render_custom_card(title, content=None, card_id=None):
    """
    Renders a custom styled card.
    
    Args:
        title: Card title
        content: Content to display (can be None if using context manager)
        card_id: Unique ID for the card
        
    Returns:
        streamlit container if content is None
    """
    st.markdown(f"""
    <div class="card-header">{title}</div>
    """, unsafe_allow_html=True)
    
    container = st.container()
    
    if content is not None:
        with container:
            st.markdown(content, unsafe_allow_html=True)
    
    return container


def render_metric_card(label, value, delta=None, unit="", help_text=""):
    """
    Renders a styled metric card with optional delta.
    
    Args:
        label: Metric label
        value: Metric value (number)
        delta: Delta value (optional)
        unit: Unit of measurement
        help_text: Help text on hover
    """
    if delta is not None:
        st.metric(
            label=label,
            value=f"{value:.1f} {unit}",
            delta=f"{delta:+.1f}%",
            help=help_text
        )
    else:
        st.metric(
            label=label,
            value=f"{value:.1f} {unit}",
            help=help_text
        )


def render_reference_card(citation, year, doi, metric_name, metric_value, source_type):
    """
    Renders a scientific reference card.
    
    Args:
        citation: Author names (e.g., "Silva et al.")
        year: Publication year
        doi: DOI link
        metric_name: Name of the measured parameter
        metric_value: Value reported
        source_type: Type of study (e.g., "Lab experiment", "Field study")
    """
    st.markdown(f"""
    <div class="reference-card">
        <div class="reference-card-title">{citation} ({year})</div>
        <div class="reference-card-meta">
            <strong>{metric_name}:</strong> {metric_value}<br>
            <em>Source:</em> {source_type}
        </div>
        <a href="https://doi.org/{doi}" target="_blank" class="reference-card-link">
            DOI: {doi} →
        </a>
    </div>
    """, unsafe_allow_html=True)


def render_badge(text, badge_type="info"):
    """
    Renders a styled badge.
    
    Args:
        text: Badge text
        badge_type: Type of badge ("success", "info", "warning")
    """
    st.markdown(f"""
    <span class="badge badge-{badge_type}">{text}</span>
    """, unsafe_allow_html=True)


def render_two_column_layout(left_content_fn, right_content_fn, ratio=[1, 1]):
    """
    Helper for two-column layouts with custom content.
    
    Args:
        left_content_fn: Function to render left column content
        right_content_fn: Function to render right column content
        ratio: Column width ratio
    """
    col1, col2 = st.columns(ratio)
    
    with col1:
        left_content_fn()
    
    with col2:
        right_content_fn()


def render_data_availability_warning(message="Data not available in curated literature"):
    """
    Renders a professional "no data" warning.
    
    Args:
        message: Warning message to display
    """
    st.markdown(f"""
    <div style="
        background-color: #FFF4E6;
        border-left: 4px solid #FF6B6B;
        padding: 16px 20px;
        border-radius: 8px;
        margin: 16px 0;
    ">
        <p style="margin: 0; color: #0F1A2A;">
            <strong>⚠️ Note:</strong> {message}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_section_divider():
    """
    Renders a styled section divider.
    """
    st.markdown("<hr>", unsafe_allow_html=True)


def render_info_box(title, content, icon="ℹ️"):
    """
    Renders an informational box.
    
    Args:
        title: Box title
        content: Box content
        icon: Icon to display
    """
    st.markdown(f"""
    <div style="
        background-color: #F5F7FA;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
    ">
        <h4 style="margin-top: 0; color: #0F1A2A;">
            {icon} {title}
        </h4>
        <p style="margin-bottom: 0; color: #0F1A2A; line-height: 1.6;">
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_loading_state(message="Loading data..."):
    """
    Renders a loading state with custom styling.
    
    Args:
        message: Loading message
    """
    with st.spinner(message):
        st.empty()


def render_professional_table(df, title="", download_filename=None):
    """
    Renders a professionally styled dataframe with optional download.
    
    Args:
        df: DataFrame to display
        title: Table title
        download_filename: Filename for CSV download (None = no download button)
    """
    if title:
        st.subheader(title)
    
    st.dataframe(
        df,
        width="stretch",
        height=400
    )
    
    if download_filename:
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name=download_filename,
            mime="text/csv"
        )


def create_sidebar_filters(df, filter_config):
    """
    Creates a standardized sidebar filter interface.
    
    Args:
        df: DataFrame with data
        filter_config: Dict specifying which filters to show
            Example: {
                'crop': True,
                'region': True,
                'year_range': [2000, 2024]
            }
            
    Returns:
        dict: Selected filter values
    """
    st.sidebar.header("🔍 Filters")
    
    filters = {}
    
    if filter_config.get('crop'):
        filters['crop'] = st.sidebar.multiselect(
            "Crop Type",
            options=df['crop'].unique() if 'crop' in df.columns else [],
            default=df['crop'].unique() if 'crop' in df.columns else []
        )
    
    if filter_config.get('region'):
        filters['region'] = st.sidebar.multiselect(
            "Region",
            options=df['region'].unique() if 'region' in df.columns else [],
            default=df['region'].unique() if 'region' in df.columns else []
        )
    
    if 'year_range' in filter_config:
        min_year, max_year = filter_config['year_range']
        filters['year_range'] = st.sidebar.slider(
            "Publication Year",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
    
    return filters


def render_comparison_metrics(current_value, baseline_value, metric_name, unit):
    """
    Renders a comparison between current and baseline values.
    
    Args:
        current_value: Current metric value
        baseline_value: Baseline/average value
        metric_name: Name of the metric
        unit: Unit of measurement
        
    Returns:
        Percentage difference
    """
    if baseline_value > 0:
        pct_diff = ((current_value - baseline_value) / baseline_value) * 100
    else:
        pct_diff = 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label=f"Current {metric_name}",
            value=f"{current_value:.1f} {unit}"
        )
    
    with col2:
        st.metric(
            label="vs Baseline",
            value=f"{baseline_value:.1f} {unit}",
            delta=f"{pct_diff:+.1f}%"
        )
    
    return pct_diff

