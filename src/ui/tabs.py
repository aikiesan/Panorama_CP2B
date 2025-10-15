"""
Simple Dropdown Navigation - Minimalistic Design
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Replaces tabs with clean, simple dropdowns for better UX
Single Responsibility: Dropdown-based sector and residue selection
"""

import streamlit as st
from typing import Tuple, Optional

from src.data.residue_registry import (
    get_residues_by_sector,
    get_residue_icon,
    get_all_sectors
)


def render_sector_tabs(key_prefix: str = "sector_tabs") -> Tuple[Optional[str], Optional[str]]:
    """
    Simple minimalistic dropdown navigation for 4 sectors.

    Uses dropdowns instead of tabs for more reliable state management in Streamlit.
    User requested: "Simple navigation tabs with minimalistic design for 4 sectors"

    Implementation: Clean dropdown selectors (more reliable than tabs in Streamlit)

    Args:
        key_prefix: Unique prefix for component keys

    Returns:
        Tuple of (selected_sector, selected_residue)
        Both can be None if nothing is selected
    """

    st.markdown("### 🎯 Selecione o Setor e Resíduo")

    # Get all sectors
    sectors = get_all_sectors()
    available_sectors = [name for name, info in sectors.items() if info.get("residues")]

    if not available_sectors:
        st.warning("⏳ Nenhum setor disponível no momento")
        return None, None

    # Add "empty" sectors to show they're coming soon
    all_sector_names = ["Agricultura", "Pecuária", "Urbano", "Industrial"]

    # Create two columns for side-by-side dropdowns
    col1, col2 = st.columns([1, 1])

    with col1:
        # Sector selection
        selected_sector = st.selectbox(
            "**Setor:**",
            all_sector_names,
            format_func=lambda x: f"{sectors[x]['icon']} {x}" if x in sectors else f"🔒 {x} (Em breve)",
            key=f"{key_prefix}_sector",
            help="Selecione o setor de origem dos resíduos"
        )

    with col2:
        # Residue selection (depends on sector)
        if selected_sector and selected_sector in available_sectors:
            residues = get_residues_by_sector(selected_sector)

            if residues:
                selected_residue = st.selectbox(
                    "**Resíduo:**",
                    residues,
                    format_func=lambda x: f"{get_residue_icon(x)} {x}",
                    key=f"{key_prefix}_residue_{selected_sector}",  # Include sector in key for proper reset
                    help=f"Selecione o resíduo do setor {selected_sector}"
                )

                # Show sector info below
                if selected_residue:
                    render_simple_residue_info(selected_sector)

                return selected_sector, selected_residue
            else:
                st.info(f"⏳ Nenhum resíduo disponível para {selected_sector}")
                return selected_sector, None
        else:
            # Sector not available yet
            st.info("⏳ **Setor em desenvolvimento**\n\nEste setor será adicionado em breve!")
            return selected_sector, None

    return None, None


def render_simple_residue_info(sector_name: str) -> None:
    """
    Display simple info about selected sector

    Args:
        sector_name: Name of the selected sector
    """
    sectors = get_all_sectors()
    sector = sectors.get(sector_name)

    if sector:
        st.markdown(
            f"""
            <div style='background: {sector["gradient"]};
                        padding: 0.8rem;
                        border-radius: 10px;
                        border-left: 4px solid {sector["border_color"]};
                        margin-top: 1rem;'>
                <p style='margin: 0; color: {sector["color"]}; font-weight: 600; font-size: 0.95rem;'>
                    {sector["icon"]} Setor: {sector["name"]}
                </p>
                <p style='margin: 0.4rem 0 0 0; color: #6b7280; font-size: 0.85rem;'>
                    {sector["description"]}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
