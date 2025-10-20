"""
Main Navigation Bar Component - Consistent across all pages
Phase 5 - Redesigned for visual appeal and usability
"""

import streamlit as st


def render_main_navigation(current_page: str = "home"):
    """
    Render the main horizontal navigation bar for all pages.

    Args:
        current_page: Current page identifier for highlighting
                     Options: "home", "disponibilidade", "parametros", "referencias",
                             "comparacao", "analise", "setores"
    """

    # Define navigation items with styling
    nav_items = [
        {
            "label": "📊 Disponibilidade",
            "page": "pages/1_📊_Disponibilidade.py",
            "key": "disp",
            "color": "#2563eb"  # Blue
        },
        {
            "label": "🧪 Parâmetros",
            "page": "pages/2_🧪_Parametros_Quimicos.py",
            "key": "param",
            "color": "#7c3aed"  # Purple
        },
        {
            "label": "📚 Referências",
            "page": "pages/3_📚_Referencias_Cientificas.py",
            "key": "ref",
            "color": "#f59e0b"  # Amber
        },
        {
            "label": "🔬 Lab Comparação",
            "page": "pages/4_🔬_Comparacao_Laboratorial.py",
            "key": "lab",
            "color": "#06b6d4"  # Cyan
        },
        {
            "label": "📈 Análise Comp.",
            "page": "pages/3_📈_Análise_Comparativa.py",
            "key": "analise",
            "color": "#ec4899"  # Pink
        },
        {
            "label": "🏭 Setores",
            "page": "pages/4_🏭_Análise_de_Setores.py",
            "key": "setores",
            "color": "#6366f1"  # Indigo
        },
    ]

    # Render navigation with columns
    nav_cols = st.columns(6, gap="medium")

    for idx, (col, nav_item) in enumerate(zip(nav_cols, nav_items)):
        with col:
            # Create a styled button
            button_style = f"""
            <style>
            .nav-btn-{nav_item['key']} {{
                display: block;
                width: 100%;
                padding: 12px 8px;
                background: linear-gradient(135deg, {nav_item['color']}dd 0%, {nav_item['color']} 100%);
                color: white;
                text-align: center;
                border-radius: 8px;
                font-weight: 600;
                font-size: 0.9rem;
                text-decoration: none;
                border: 2px solid {nav_item['color']};
                transition: all 0.3s ease;
                cursor: pointer;
            }}
            .nav-btn-{nav_item['key']}:hover {{
                background: linear-gradient(135deg, {nav_item['color']} 0%, {nav_item['color']}ee 100%);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                border-color: {nav_item['color']};
            }}
            </style>
            """

            st.markdown(button_style, unsafe_allow_html=True)

            if st.button(nav_item["label"], key=f"nav_{nav_item['key']}", use_container_width=True):
                st.switch_page(nav_item["page"])


def render_navigation_divider():
    """Render a visual divider after navigation bar"""
    st.markdown("---")
