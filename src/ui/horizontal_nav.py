"""
Horizontal Navigation Component
CP2B - Provides page navigation tabs below header
"""

import streamlit as st


def render_horizontal_nav(current_page: str = "Disponibilidade"):
    """
    Render horizontal navigation tabs for all pages

    Args:
        current_page: Name of the current page (for highlighting)
                     Options: "Disponibilidade", "Parametros", "Referencias", "Lab"
    """
    nav_items = [
        {"name": "Disponibilidade", "icon": "📊", "path": "pages/1_📊_Disponibilidade.py"},
        {"name": "Parametros", "icon": "🧪", "path": "pages/2_🧪_Parametros_Quimicos.py"},
        {"name": "Referencias", "icon": "📚", "path": "pages/3_📚_Referencias_Cientificas.py"},
        {"name": "Lab", "icon": "🔬", "path": "pages/4_🔬_Comparacao_Laboratorial.py"},
    ]

    st.markdown('<div class="nav-tabs-container">', unsafe_allow_html=True)
    cols = st.columns(len(nav_items))

    for idx, (col, item) in enumerate(zip(cols, nav_items)):
        with col:
            is_active = item["name"] == current_page
            button_label = f"{item['icon']} {item['name']}"
            
            if st.button(
                button_label, 
                key=f"nav_{item['name']}", 
                use_container_width=True,
                disabled=is_active
            ):
                if not is_active:
                    st.switch_page(item['path'])
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")


def render_horizontal_nav_pills(current_page: str = "Disponibilidade"):
    """
    Alternative implementation using st.pills (Streamlit native component)
    Simpler but less customizable

    Args:
        current_page: Name of the current page (for highlighting)
    """
    nav_options = {
        "📊 Disponibilidade": "pages/1_📊_Disponibilidade.py",
        "🧪 Parâmetros": "pages/2_🧪_Parametros_Quimicos.py",
        "📚 Referências": "pages/3_📚_Referencias_Cientificas.py",
        "🔬 Lab Comparação": "pages/4_🔬_Comparacao_Laboratorial.py",
    }

    # Map current page to option
    page_map = {
        "Disponibilidade": "📊 Disponibilidade",
        "Parametros": "🧪 Parâmetros",
        "Referencias": "📚 Referências",
        "Lab": "🔬 Lab Comparação",
    }

    default_selection = page_map.get(current_page, "📊 Disponibilidade")

    # Center the pills
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        selected = st.pills(
            "Navegação",
            options=list(nav_options.keys()),
            default=default_selection,
            label_visibility="collapsed"
        )

        # Navigate if selection changed
        if selected != default_selection:
            st.switch_page(nav_options[selected])

    st.markdown("---")
