"""
PanoramaCP2B - Centro Paulista de Estudos em Biogás e Bioprodutos
Homepage - Laboratory Validation Tool for Biogas Research
Phase 5 Complete Edition - Enhanced UI/UX
"""

import streamlit as st
from src.ui.main_navigation import render_main_navigation, render_navigation_divider
from src.ui.homepage_components import (
    render_hero_section,
    render_about_section,
    render_phase5_highlights,
    render_features_grid,
    render_saf_priority_summary,
    render_sector_overview,
    render_footer
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="PanoramaCP2B - Validação Laboratorial | Phase 5 Complete",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# RENDER HOMEPAGE COMPONENTS (SOLID ARCHITECTURE)
# ============================================================================

# Hero section with platform title and Phase 5 statistics
render_hero_section()

# Horizontal navigation bar
render_main_navigation(current_page="home")
render_navigation_divider()

# About platform section
render_about_section()

# Phase 5 completion highlights
render_phase5_highlights()

# Main features grid (2 columns)
render_features_grid()

# Link to Metodologia page
st.info("📖 **Metodologia Completa**: Para informações detalhadas sobre a metodologia SAF, fontes de dados, "
        "e processos de cálculo, visite a página [📖 Metodologia](#) na barra lateral.")

st.markdown("---")

# SAF priority summary with metrics
render_saf_priority_summary()

# Sector overview with top performers
render_sector_overview()

# Footer
render_footer()
