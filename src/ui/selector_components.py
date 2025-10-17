"""
Selector Components Module - Single Responsibility Principle
Reusable sector and residue selector components.
"""

import streamlit as st
from typing import Optional


def render_sector_selector(key_prefix: str = "sector") -> Optional[str]:
    """
    Render parallel sector selection cards.

    Args:
        key_prefix: Unique prefix for component keys

    Returns:
        Selected sector name or None
    """
    from src.data.residue_registry import get_all_sectors

    st.markdown("### 🎯 Selecionar Setor")
    st.markdown("Escolha o setor de origem dos resíduos para análise:")

    sectors = get_all_sectors()

    # Get all 4 sectors (including empty ones for future)
    all_sector_names = ["Agricultura", "Pecuária", "Urbano", "Industrial"]

    # Initialize session state
    session_key = f"{key_prefix}_selected"
    if session_key not in st.session_state:
        st.session_state[session_key] = None

    # Add smooth scroll JavaScript
    st.markdown("""
    <script>
    function smoothScrollDown() {
        window.scrollBy({
            top: 400,
            behavior: 'smooth'
        });
    }
    </script>
    """, unsafe_allow_html=True)

    # Create 4 compact cards in a single row
    cols = st.columns(4)

    for idx, sector_name in enumerate(all_sector_names):
        sector = sectors.get(sector_name)
        if not sector:
            continue

        with cols[idx]:
            # Check if sector has residues and if it's selected
            has_residues = len(sector["residues"]) > 0
            is_selected = st.session_state[session_key] == sector_name
            opacity_style = "" if has_residues else "opacity: 0.5;"
            cursor_style = "cursor: pointer;" if has_residues else "cursor: not-allowed;"

            # Add selection indicator styling
            selected_border = "3px" if is_selected else "2px"
            selected_shadow = "0 4px 12px rgba(37, 99, 235, 0.3)" if is_selected else "0 2px 8px rgba(0,0,0,0.08)"

            # Selection checkmark (only if selected)
            checkmark = f'<div style="position: absolute; top: 0.3rem; right: 0.3rem; background: rgba(37, 99, 235, 0.9); color: white; border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; z-index: 2;">✓</div>' if is_selected else ''

            # Container wrapper for card + button overlay
            st.markdown(f'<div class="sector-card-container" data-sector="{sector_name}">', unsafe_allow_html=True)

            # Compact clickable sector card
            html_content = (
                f'<div id="sector_{sector_name}" class="sector-card {("selected" if is_selected else "")}" style="'
                f'background: {sector["gradient"]}; '
                f'padding: 0.7rem 0.5rem; '
                f'border-radius: 14px; '
                f'border: {selected_border} solid {sector["border_color"]}; '
                f'text-align: center; '
                f'min-height: 100px; '
                f'box-shadow: {selected_shadow}; '
                f'{cursor_style} '
                f'{opacity_style} '
                f'margin-bottom: 0; '
                f'display: flex; '
                f'flex-direction: column; '
                f'justify-content: center; '
                f'align-items: center; '
                f'position: relative; '
                f'transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease; '
                f'pointer-events: none;">'
                f'{checkmark}'
                f'<div style="font-size: 2rem; margin-bottom: 0.25rem; line-height: 1;">{sector["icon"]}</div>'
                f'<h4 style="color: {sector["color"]}; margin: 0.15rem 0; font-weight: 700; font-size: 0.95rem; line-height: 1.2; white-space: nowrap;">'
                f'{sector["name"]}'
                f'</h4>'
                f'<p style="color: #4b5563; font-size: 0.7rem; margin: 0.2rem 0.4rem; line-height: 1.2; max-width: 100%; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; white-space: normal;">'
                f'{sector["description"]}'
                f'</p>'
                f'<p style="color: {sector["color"]}; font-size: 0.75rem; margin: 0.25rem 0 0 0; font-weight: 700; background: rgba(255,255,255,0.6); padding: 0.15rem 0.5rem; border-radius: 10px;">'
                f'📊 {len(sector["residues"])} resíduo{"s" if len(sector["residues"]) != 1 else ""}'
                f'</p>'
                f'</div>'
            )
            st.markdown(html_content, unsafe_allow_html=True)

            # Invisible button overlay - positioned absolutely over the card
            if has_residues:
                if st.button(
                    sector['name'],  # Hidden by CSS
                    key=f"{key_prefix}_btn_{sector_name}",
                    width="stretch",
                    type="primary" if is_selected else "secondary",
                    help=f"Clique para selecionar {sector['name']}"
                ):
                    st.session_state[session_key] = sector_name
                    st.markdown("""
                    <script>
                    setTimeout(function() {
                        window.scrollBy({
                            top: 350,
                            behavior: 'smooth'
                        });
                    }, 100);
                    </script>
                    """, unsafe_allow_html=True)
                    st.rerun()
            else:
                st.button(
                    sector['name'],
                    key=f"{key_prefix}_btn_disabled_{sector_name}",
                    width="stretch",
                    disabled=True,
                    help=f"O setor {sector_name} será adicionado em breve"
                )

            st.markdown('</div>', unsafe_allow_html=True)  # Close container

    # Integrated card styling - button overlays card
    st.markdown("""
    <style>
    /* Container for card + button */
    .sector-card-container {
        position: relative;
        margin-bottom: 1rem;
    }

    /* Hover effect on container affects card */
    .sector-card-container:hover .sector-card:not([style*="opacity: 0.5"]) {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15) !important;
        border-width: 3px !important;
    }

    /* Disabled sector cards */
    .sector-card[style*="opacity: 0.5"] {
        filter: grayscale(0.3);
    }

    /* Position button absolutely over the card */
    .sector-card-container div[data-testid="stButton"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        z-index: 1;
    }

    /* Make button invisible but clickable */
    .sector-card-container button {
        width: 100% !important;
        height: 100% !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: transparent !important;
        font-size: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        min-height: unset !important;
        cursor: pointer !important;
        border-radius: 14px !important;
    }

    .sector-card-container button:hover {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    .sector-card-container button[kind="primary"],
    .sector-card-container button[kind="secondary"] {
        background: transparent !important;
        border: none !important;
    }

    .sector-card-container button:disabled {
        cursor: not-allowed !important;
        background: transparent !important;
        opacity: 1 !important;
    }

    /* Prevent button focus outline from showing */
    .sector-card-container button:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    /* Ensure checkmark stays on top */
    .sector-card > div[style*="z-index: 2"] {
        pointer-events: none;
    }
    </style>
    """, unsafe_allow_html=True)

    return st.session_state[session_key]


def render_residue_selector_for_sector(
    sector_name: str,
    key_prefix: str = "residue"
) -> Optional[str]:
    """
    Render residue selection dropdown for a specific sector.

    Args:
        sector_name: Name of the selected sector
        key_prefix: Unique prefix for component keys

    Returns:
        Selected residue name or None
    """
    from src.data.residue_registry import (
        get_sector_info,
        get_residues_by_sector,
        get_residue_icon
    )

    sector = get_sector_info(sector_name)
    if not sector:
        st.error(f"⚠️ Setor '{sector_name}' não encontrado")
        return None

    residues = get_residues_by_sector(sector_name)

    if not residues:
        st.info(f"ℹ️ Nenhum resíduo disponível para o setor **{sector_name}** ainda")
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

    # Residue selector
    st.markdown("### 🌾 Selecionar Resíduo")

    selected_residue = st.selectbox(
        "**Resíduo/Cultura:**",
        residues,
        format_func=lambda x: f"{get_residue_icon(x)} {x}",
        key=f"{key_prefix}_select_{sector_name}"
    )

    return selected_residue


def render_full_selector(key_prefix: str = "selector") -> Optional[str]:
    """
    Render complete sector + residue selector workflow with session state.

    Args:
        key_prefix: Unique prefix for component keys

    Returns:
        Selected residue name or None
    """
    # Initialize session state
    sector_key = f"{key_prefix}_selected_sector"
    if sector_key not in st.session_state:
        st.session_state[sector_key] = None

    # Show sector selector
    selected_sector = render_sector_selector(key_prefix=f"{key_prefix}_sector")

    # Show residue selector if sector is selected
    if selected_sector or st.session_state[sector_key]:
        # Update session state
        if selected_sector:
            st.session_state[sector_key] = selected_sector

        st.markdown("---")

        # Button to change sector
        if st.button("🔄 Trocar Setor", key=f"{key_prefix}_change_sector"):
            st.session_state[sector_key] = None
            st.rerun()

        return render_residue_selector_for_sector(
            st.session_state[sector_key],
            key_prefix=f"{key_prefix}_residue"
        )

    return None


__all__ = [
    'render_sector_selector',
    'render_residue_selector_for_sector',
    'render_full_selector'
]
