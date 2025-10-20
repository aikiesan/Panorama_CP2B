"""
Hierarchical Selector Component - 3-Level Complete Integration
Phase 5: Sector -> Culture -> Residue

This module provides the complete 3-level hierarchical selector workflow
"""

import streamlit as st
from typing import Optional


def render_full_selector_3_levels(key_prefix: str = "hierarchical") -> Optional[str]:
    """
    Render complete 3-level hierarchical selector workflow with session state.

    Flow: Sector -> Culture -> Residue

    Args:
        key_prefix: Unique prefix for component keys

    Returns:
        Selected residue name or None

    Example:
        ```python
        from src.ui.hierarchical_selector import render_full_selector_3_levels

        selected_residue_name = render_full_selector_3_levels(key_prefix="page1")

        if selected_residue_name:
            residue_data = get_residue_data(selected_residue_name)
            # ... use residue data
        ```
    """
    from .selector_components import render_sector_selector
    from .culture_selector import (
        render_culture_selector,
        render_residue_selector_for_culture
    )

    # Initialize session state keys
    sector_key = f"{key_prefix}_selected_sector"
    culture_key = f"{key_prefix}_selected_culture"

    if sector_key not in st.session_state:
        st.session_state[sector_key] = None
    if culture_key not in st.session_state:
        st.session_state[culture_key] = None

    # ====================================================================
    # LEVEL 1: SECTOR SELECTION
    # ====================================================================

    st.markdown("## 🎯 Seleção Hierárquica de Resíduos")
    st.markdown("Selecione o setor, cultura e resíduo específico para análise")

    selected_sector = render_sector_selector(key_prefix=f"{key_prefix}_sector")

    # ====================================================================
    # LEVEL 2: CULTURE SELECTION (if sector is selected)
    # ====================================================================

    if selected_sector or st.session_state[sector_key]:
        # Update session state
        if selected_sector:
            # Sector changed - reset culture selection
            if st.session_state[sector_key] != selected_sector:
                st.session_state[culture_key] = None
            st.session_state[sector_key] = selected_sector

        st.markdown("---")

        # Button to change sector
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("🔄 Trocar Setor", key=f"{key_prefix}_change_sector"):
                st.session_state[sector_key] = None
                st.session_state[culture_key] = None
                st.rerun()

        # Render culture selector
        selected_culture = render_culture_selector(
            st.session_state[sector_key],
            key_prefix=f"{key_prefix}_culture"
        )

        # ================================================================
        # LEVEL 3: RESIDUE SELECTION (if culture is selected)
        # ================================================================

        if selected_culture or st.session_state[culture_key]:
            # Update session state
            if selected_culture:
                # Culture changed
                st.session_state[culture_key] = selected_culture

            st.markdown("---")

            # Buttons to change sector or culture
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("🔄 Trocar Cultura", key=f"{key_prefix}_change_culture"):
                    st.session_state[culture_key] = None
                    st.rerun()

            # Render residue selector
            selected_residue = render_residue_selector_for_culture(
                st.session_state[sector_key],
                st.session_state[culture_key],
                key_prefix=f"{key_prefix}_residue"
            )

            return selected_residue

    return None


def render_quick_selector_with_hierarchy(
    default_sector: Optional[str] = None,
    default_culture: Optional[str] = None,
    key_prefix: str = "quick"
) -> Optional[str]:
    """
    Render a quick selector with optional defaults for sector and culture.
    Useful for pages that want to start at a specific point in the hierarchy.

    Args:
        default_sector: Optional default sector to pre-select
        default_culture: Optional default culture to pre-select
        key_prefix: Unique prefix for component keys

    Returns:
        Selected residue name or None

    Example:
        ```python
        # Start with Agricultura -> Cana-de-Açúcar pre-selected
        residue = render_quick_selector_with_hierarchy(
            default_sector="Agricultura",
            default_culture="Cana-de-Açúcar",
            key_prefix="quick1"
        )
        ```
    """
    from .selector_components import render_sector_selector
    from .culture_selector import (
        render_culture_selector,
        render_residue_selector_for_culture
    )

    # Initialize session state with defaults
    sector_key = f"{key_prefix}_selected_sector"
    culture_key = f"{key_prefix}_selected_culture"

    if sector_key not in st.session_state:
        st.session_state[sector_key] = default_sector
    if culture_key not in st.session_state:
        st.session_state[culture_key] = default_culture

    # If we have defaults, start directly at culture or residue level
    if st.session_state[sector_key] and st.session_state[culture_key]:
        # Show breadcrumb
        st.markdown(f"""
        **Seleção atual:** {st.session_state[sector_key]} → {st.session_state[culture_key]}
        """)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Trocar Setor/Cultura", key=f"{key_prefix}_reset"):
                st.session_state[sector_key] = None
                st.session_state[culture_key] = None
                st.rerun()

        return render_residue_selector_for_culture(
            st.session_state[sector_key],
            st.session_state[culture_key],
            key_prefix=f"{key_prefix}_residue"
        )

    elif st.session_state[sector_key]:
        # Show sector, select culture
        st.markdown(f"**Setor selecionado:** {st.session_state[sector_key]}")

        if st.button("🔄 Trocar Setor", key=f"{key_prefix}_change_sector"):
            st.session_state[sector_key] = None
            st.rerun()

        selected_culture = render_culture_selector(
            st.session_state[sector_key],
            key_prefix=f"{key_prefix}_culture"
        )

        if selected_culture:
            st.session_state[culture_key] = selected_culture
            st.rerun()

    else:
        # Start from scratch - select sector
        return render_full_selector_3_levels(key_prefix=key_prefix)

    return None


__all__ = [
    'render_full_selector_3_levels',
    'render_quick_selector_with_hierarchy',
]
