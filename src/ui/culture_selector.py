"""
Culture Selector Component - 3-Level Hierarchy Support
Phase 5: Hierarchical Organization (Sector -> Culture -> Residue)
"""

import streamlit as st
from typing import Optional


def render_culture_selector(
    sector_name: str,
    key_prefix: str = "culture"
) -> Optional[str]:
    """
    Render culture selection dropdown for a specific sector.
    This is the 2nd level of the 3-level hierarchy: Sector -> Culture -> Residue

    Args:
        sector_name: Name of the selected sector
        key_prefix: Unique prefix for component keys

    Returns:
        Selected culture name or None
    """
    from src.data.culture_hierarchy import (
        get_cultures_by_sector,
        get_culture_metadata,
        get_culture_icon
    )
    from src.data.residue_registry import get_sector_info

    sector = get_sector_info(sector_name)
    if not sector:
        st.error(f"⚠️ Setor '{sector_name}' não encontrado")
        return None

    cultures = get_cultures_by_sector(sector_name)

    if not cultures:
        st.info(f"ℹ️ Nenhuma cultura disponível para o setor **{sector_name}** ainda")
        return None

    # Display selected sector info
    st.markdown(f"""
    <div style='background: {sector["gradient"]};
                padding: 1.2rem;
                border-radius: 12px;
                border-left: 6px solid {sector["border_color"]};
                margin-bottom: 1.5rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
        <p style='margin: 0; color: {sector["color"]}; font-weight: 700; font-size: 1.1rem;'>
            {sector["icon"]} Setor Selecionado: {sector["name"]}
        </p>
        <p style='margin: 0.6rem 0 0 0; color: #4b5563; font-size: 0.95rem;'>
            {sector["description"]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Culture selector
    st.markdown("### 🌾 Selecionar Cultura")

    selected_culture = st.selectbox(
        "**Cultura/Subsetor:**",
        cultures,
        format_func=lambda x: f"{get_culture_icon(x)} {x}",
        key=f"{key_prefix}_select_{sector_name}",
        help="Selecione a cultura ou tipo de atividade produtiva"
    )

    return selected_culture


def render_residue_selector_for_culture(
    sector_name: str,
    culture_name: str,
    key_prefix: str = "residue"
) -> Optional[str]:
    """
    Render residue selection dropdown for a specific culture.
    This is the 3rd level of the hierarchy: Sector -> Culture -> Residue

    Args:
        sector_name: Name of the selected sector
        culture_name: Name of the selected culture
        key_prefix: Unique prefix for component keys

    Returns:
        Selected residue name or None
    """
    from src.data.culture_hierarchy import (
        get_residues_by_culture,
        get_culture_metadata,
        get_culture_icon
    )
    from src.data.residue_registry import get_residue_icon

    culture_meta = get_culture_metadata(culture_name)
    if not culture_meta:
        st.error(f"⚠️ Cultura '{culture_name}' não encontrada")
        return None

    residues = get_residues_by_culture(sector_name, culture_name)

    if not residues:
        st.info(f"ℹ️ Nenhum resíduo disponível para a cultura **{culture_name}** ainda")
        return None

    # Display selected culture info
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
                padding: 1rem;
                border-radius: 10px;
                border-left: 5px solid #6b7280;
                margin-bottom: 1.5rem;
                box-shadow: 0 2px 6px rgba(0,0,0,0.06);'>
        <p style='margin: 0; color: #374151; font-weight: 700; font-size: 1rem;'>
            {get_culture_icon(culture_name)} Cultura Selecionada: {culture_name}
        </p>
        <p style='margin: 0.4rem 0 0 0; color: #6b7280; font-size: 0.9rem;'>
            {culture_meta["description"]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Residue selector with dropdown separators
    st.markdown("### 🌾 Selecionar Resíduo")

    # Format residues with separators for the dropdown
    selected_residue = st.selectbox(
        "**Resíduo:**",
        residues,
        format_func=lambda x: f"{get_residue_icon(x)} {x}",
        key=f"{key_prefix}_select_{sector_name}_{culture_name}",
        help=f"Selecione o resíduo específico de {culture_name}"
    )

    return selected_residue


__all__ = [
    'render_culture_selector',
    'render_residue_selector_for_culture',
]
