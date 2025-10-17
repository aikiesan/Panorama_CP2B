"""
Card Components Module - Single Responsibility Principle
Reusable card and visual display components.
"""

import streamlit as st
from typing import Optional


def render_info_card(title: str, content: str, icon: str = "ℹ️") -> None:
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


def render_compact_parameter_card(
    param_name: str,
    value: float,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    unit: str = "",
    icon: str = "📊"
) -> None:
    """
    Render single compact parameter card with optional range.

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


def render_gradient_card(
    title: str,
    content: str,
    icon: str = "📊",
    gradient: str = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    border_color: str = "#667eea"
) -> None:
    """
    Renders a gradient card with icon and content.

    Args:
        title: Card title
        content: Card content text
        icon: Emoji icon
        gradient: CSS gradient string
        border_color: Border color hex
    """
    st.markdown(f"""
    <div style='background: {gradient};
                padding: 1.5rem;
                border-radius: 12px;
                border: 2px solid {border_color};
                margin-bottom: 1rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{icon}</div>
        <h3 style='color: white; margin: 0.5rem 0; font-weight: 700; font-size: 1.3rem;'>
            {title}
        </h3>
        <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1rem; line-height: 1.5;'>
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_status_card(
    status: str,
    message: str,
    details: Optional[str] = None
) -> None:
    """
    Renders a status card (success, warning, error, info).

    Args:
        status: One of "success", "warning", "error", "info"
        message: Main status message
        details: Optional detailed message
    """
    status_config = {
        "success": {"icon": "✅", "color": "#059669", "bg": "#d1fae5"},
        "warning": {"icon": "⚠️", "color": "#f59e0b", "bg": "#fef3c7"},
        "error": {"icon": "❌", "color": "#dc2626", "bg": "#fee2e2"},
        "info": {"icon": "ℹ️", "color": "#2563eb", "bg": "#dbeafe"}
    }

    config = status_config.get(status, status_config["info"])

    details_html = f"<p style='margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #4b5563;'>{details}</p>" if details else ""

    st.markdown(f"""
    <div style='background: {config["bg"]};
                padding: 1.2rem;
                border-radius: 10px;
                border-left: 5px solid {config["color"]};
                margin: 1rem 0;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);'>
        <div style='display: flex; align-items: center; gap: 0.8rem;'>
            <span style='font-size: 1.5rem;'>{config["icon"]}</span>
            <p style='margin: 0; font-weight: 600; color: {config["color"]}; font-size: 1.1rem;'>
                {message}
            </p>
        </div>
        {details_html}
    </div>
    """, unsafe_allow_html=True)


def show_about_section() -> None:
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


__all__ = [
    'render_info_card',
    'render_compact_parameter_card',
    'render_gradient_card',
    'render_status_card',
    'show_about_section'
]
