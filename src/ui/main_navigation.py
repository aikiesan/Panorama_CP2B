"""
Main Navigation Bar Component - Consistent across all pages
Unified navigation for ALL 7 pages (Homepage + 6 content pages)
Following SOLID principles - Single Responsibility Principle (SRP)
"""

import streamlit as st


def render_main_navigation(current_page: str = "home"):
    """
    Render the main horizontal navigation bar for all pages.

    Args:
        current_page: Current page identifier for highlighting
                     Options: "home", "disponibilidade", "parametros", "referencias",
                             "lab", "comparativa", "setores"
    """

    # Define navigation items - ALL 7 pages (Homepage + 6 content pages)
    # Order: Início → Disponibilidade → Parâmetros → Setores → Análise Comp. → Lab → Referências
    nav_items = [
        {
            "label": "🏠 Início",
            "page": "app.py",
            "key": "home",
        },
        {
            "label": "📊 Disponibilidade",
            "page": "pages/1_📊_Disponibilidade.py",
            "key": "disponibilidade",
        },
        {
            "label": "🧪 Parâmetros",
            "page": "pages/2_🧪_Parametros_Quimicos.py",
            "key": "parametros",
        },
        {
            "label": "🏭 Setores",
            "page": "pages/4_🏭_Análise_de_Setores.py",
            "key": "setores",
        },
        {
            "label": "📈 Análise Comp.",
            "page": "pages/3_📈_Análise_Comparativa.py",
            "key": "comparativa",
        },
        {
            "label": "🔬 Lab Comparação",
            "page": "pages/4_🔬_Comparacao_Laboratorial.py",
            "key": "lab",
        },
        {
            "label": "📚 Referências",
            "page": "pages/3_📚_Referencias_Cientificas.py",
            "key": "referencias",
        },
    ]

    # Render navigation with columns (7 equal columns)
    nav_cols = st.columns(7, gap="small")

    for col, nav_item in zip(nav_cols, nav_items):
        with col:
            # Check if this is the current page
            is_current = (current_page == nav_item["key"])

            # Use Streamlit native button with disabled state for current page
            if st.button(
                nav_item["label"],
                key=f"nav_{nav_item['key']}",
                use_container_width=True,
                disabled=is_current,
                type="primary" if is_current else "secondary"
            ):
                st.switch_page(nav_item["page"])


def render_sidebar_navigation(current_page: str = "home"):
    """
    Render beautiful sidebar navigation with grouped sections.
    Follows SOLID SRP - handles only sidebar navigation rendering.

    Args:
        current_page: Current page identifier for highlighting
    """

    # Define navigation structure with logical grouping
    nav_sections = [
        {
            "title": "🏠 Principal",
            "pages": [
                {
                    "label": "Início",
                    "icon": "🏠",
                    "page": "app.py",
                    "key": "home",
                    "description": "Página inicial e metodologia"
                }
            ]
        },
        {
            "title": "📊 Dados e Análise",
            "pages": [
                {
                    "label": "Disponibilidade",
                    "icon": "📊",
                    "page": "pages/1_📊_Disponibilidade.py",
                    "key": "disponibilidade",
                    "description": "Fatores de disponibilidade SAF"
                },
                {
                    "label": "Parâmetros Químicos",
                    "icon": "🧪",
                    "page": "pages/2_🧪_Parametros_Quimicos.py",
                    "key": "parametros",
                    "description": "BMP, TS, VS e composição"
                },
                {
                    "label": "Referências Científicas",
                    "icon": "📚",
                    "page": "pages/3_📚_Referencias_Cientificas.py",
                    "key": "referencias",
                    "description": "Literatura validada e DOIs"
                }
            ]
        },
        {
            "title": "🔬 Ferramentas",
            "pages": [
                {
                    "label": "Comparação Laboratorial",
                    "icon": "🔬",
                    "page": "pages/4_🔬_Comparacao_Laboratorial.py",
                    "key": "lab",
                    "description": "Valide dados de laboratório"
                }
            ]
        },
        {
            "title": "📈 Análises Avançadas",
            "pages": [
                {
                    "label": "Análise Comparativa",
                    "icon": "📈",
                    "page": "pages/3_📈_Análise_Comparativa.py",
                    "key": "comparativa",
                    "description": "Rankings e comparações"
                },
                {
                    "label": "Análise de Setores",
                    "icon": "🏭",
                    "page": "pages/4_🏭_Análise_de_Setores.py",
                    "key": "setores",
                    "description": "Potencial por setor econômico"
                }
            ]
        }
    ]

    with st.sidebar:
        st.markdown("### 🧭 Navegação")

        # Render each section
        for section in nav_sections:
            st.markdown(f"**{section['title']}**")

            for page in section['pages']:
                is_current = (current_page == page['key'])

                # Use different button style for current page
                button_type = "primary" if is_current else "secondary"

                if st.button(
                    f"{page['icon']} {page['label']}",
                    key=f"sidebar_nav_{page['key']}",
                    use_container_width=True,
                    disabled=is_current,
                    type=button_type,
                    help=page['description']
                ):
                    st.switch_page(page['page'])

            # Add spacing between sections (except after last section)
            if section != nav_sections[-1]:
                st.markdown("")  # Small gap


def render_navigation_divider():
    """Render a visual divider after navigation bar"""
    st.markdown("---")
