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
    # Define navigation items
    nav_items = [
        {"name": "Disponibilidade", "icon": "📊", "path": "pages/1_📊_Disponibilidade.py"},
        {"name": "Parametros", "icon": "🧪", "path": "pages/2_🧪_Parametros_Quimicos.py"},
        {"name": "Referencias", "icon": "📚", "path": "pages/3_📚_Referencias_Cientificas.py"},
        {"name": "Lab", "icon": "🔬", "path": "pages/4_🔬_Comparacao_Laboratorial.py"},
    ]

    # CSS for horizontal tabs
    st.markdown("""
    <style>
    .nav-tabs-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        padding: 1.2rem 0;
        margin: -1rem 0 2rem 0;
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .nav-tab {
        flex: 1;
        max-width: 200px;
        padding: 0.9rem 1.2rem;
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        color: #374151;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }

    .nav-tab:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-color: #9ca3af;
    }

    .nav-tab-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }

    .nav-tab-active:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    .nav-icon {
        font-size: 1.5rem;
        display: block;
        margin-bottom: 0.3rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create columns for navigation
    cols = st.columns(len(nav_items))

    for idx, (col, item) in enumerate(zip(cols, nav_items)):
        with col:
            is_active = item["name"] == current_page
            button_label = f"{item['icon']} {item['name']}"

            # Use different button types based on active state
            if is_active:
                st.markdown(f"""
                <div class="nav-tab nav-tab-active">
                    <span class="nav-icon">{item['icon']}</span>
                    <div>{item['name']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(button_label, key=f"nav_{item['name']}", use_container_width=True):
                    st.switch_page(item['path'])

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
