"""
Availability Card Component
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Display expanded residue availability information with sub-components

This component renders a comprehensive card showing:
- Residue name and generation rate
- Current destination/use
- Methane potential and moisture
- Availability factors with MIN/MEAN/MAX ranges
- Final availability percentage
- Sub-residues (if composite residue)
- Technical justification (collapsible)
- Performance metrics

SOLID Compliance:
- Single Responsibility: Only renders availability information
- Open/Closed: Extensible for new residue types
- No business logic: Pure UI rendering
"""

import streamlit as st
from typing import Optional
from src.models.residue_models import ResidueData
from src.utils.formatters import format_number, format_biogas_potential, format_electricity_potential


def render_availability_card(
    residue_data: ResidueData,
    scenario: str = 'Realista',
    expand_sub_residues: bool = True,
    show_justification: bool = True
) -> None:
    """
    Render expanded availability card for a residue/sub-residue.

    Displays comprehensive residue information including:
    - Generation and destination
    - Chemical parameters (BMP, TS, VS, Moisture)
    - Availability factors with ranges
    - Final calculated availability %
    - Sub-residues (if composite)
    - Technical justification

    Args:
        residue_data: ResidueData object with all parameters
        scenario: Which scenario to display ('Pessimista', 'Realista', 'Otimista', 'Teórico')
        expand_sub_residues: Show sub-residues details (default True)
        show_justification: Show technical justification (default True)

    Returns:
        None (renders to Streamlit UI)

    Example:
        >>> from src.data.agricultura.cana_palha import PALHA_DE_CANA_DE_ACUCAR_PALHICO_DATA
        >>> render_availability_card(
        ...     PALHA_DE_CANA_DE_ACUCAR_PALHICO_DATA,
        ...     scenario='Realista'
        ... )
    """
    with st.container():
        # Header with residue name and icon
        col1, col2, col3 = st.columns([1, 6, 2])
        with col1:
            st.markdown(f"## {residue_data.icon}")
        with col2:
            st.markdown(f"### {residue_data.name}")
        with col3:
            availability_pct = residue_data.availability.final_availability
            color = "green" if availability_pct > 30 else "orange" if availability_pct > 10 else "red"
            st.markdown(f"**Disponibilidade:** :{color}[{availability_pct:.1f}%]")

        st.divider()

        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Geração",
                residue_data.generation.split("|")[0].strip() if "|" in residue_data.generation else residue_data.generation[:20]
            )

        with col2:
            ch4_potential = residue_data.scenarios.get(scenario, 0.0)
            st.metric(
                f"Biogás ({scenario})",
                format_biogas_potential(ch4_potential)
            )

        with col3:
            # Calculate electricity from CH4 (1 Nm³ CH4 ≈ 1 kWh at 40% efficiency)
            electricity_gwh = ch4_potential / 1_000_000 * 1.44 / 1_000  # Nm³ to GWh
            st.metric(
                "Eletricidade Potencial",
                f"{electricity_gwh:.2f} GWh" if electricity_gwh > 0 else "N/A"
            )

        with col4:
            st.metric(
                "Umidade",
                f"{residue_data.chemical_params.moisture:.1f}%"
            )

        st.divider()

        # ===== MAIN SECTION: Availability Factors (Primary Focus) =====
        with st.expander("✅ Fatores de Disponibilidade", expanded=True):
            _render_availability_factors(residue_data, scenario)

        st.divider()

        # ===== SECONDARY SECTIONS: Supporting Details =====

        # Operational Parameters
        with st.expander("🔧 Parâmetros Operacionais", expanded=False):
            _render_operational_parameters(residue_data)

        # Current Destination
        with st.expander("🎯 Destino Atual", expanded=False):
            st.markdown(residue_data.destination)

        # Technical Justification
        if show_justification:
            with st.expander("📝 Justificativa Técnica", expanded=False):
                st.markdown(residue_data.justification)

        # Scientific References
        if residue_data.references:
            with st.expander(f"📚 Referências Científicas ({len(residue_data.references)})", expanded=False):
                _render_references(residue_data.references)

        st.divider()

        # Sub-residues section (if composite)
        if residue_data.has_sub_residues() and expand_sub_residues:
            st.markdown("### 🔬 Sub-Resíduos Componentes")
            _render_sub_residues_summary(residue_data, scenario)


def _render_chemical_parameters(residue_data: ResidueData) -> None:
    """Render chemical parameters table with ranges."""
    import pandas as pd

    # Create range table
    param_table = residue_data.chemical_params.to_range_table()

    if param_table:
        df = pd.DataFrame(param_table)
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            column_config={
                "Parâmetro": st.column_config.TextColumn(width="large"),
                "Mínimo": st.column_config.TextColumn(width="small"),
                "Média/Valor": st.column_config.TextColumn(width="small"),
                "Máximo": st.column_config.TextColumn(width="small"),
                "Unidade": st.column_config.TextColumn(width="small"),
            }
        )
    else:
        st.info("Sem dados de parâmetros químicos disponíveis")


def _render_operational_parameters(residue_data: ResidueData) -> None:
    """Render operational parameters table with ranges."""
    import pandas as pd

    # Create range table
    param_table = residue_data.operational.to_range_table()

    if param_table:
        df = pd.DataFrame(param_table)
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            column_config={
                "Parâmetro": st.column_config.TextColumn(width="large"),
                "Mínimo": st.column_config.TextColumn(width="small"),
                "Valor Operacional": st.column_config.TextColumn(width="medium"),
                "Máximo": st.column_config.TextColumn(width="small"),
            }
        )
    else:
        st.info("Sem dados de parâmetros operacionais disponíveis")


def _render_availability_factors(residue_data: ResidueData, scenario: str) -> None:
    """Render availability factors with MIN/MEAN/MAX ranges."""
    import pandas as pd

    # Create availability factors range table
    factor_table = residue_data.availability.to_range_table()

    if factor_table:
        df = pd.DataFrame(factor_table)
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            column_config={
                "Fator": st.column_config.TextColumn(width="large"),
                "Mínimo": st.column_config.TextColumn(width="small"),
                "Valor Adotado": st.column_config.TextColumn(width="small"),
                "Máximo": st.column_config.TextColumn(width="small"),
                "Justificativa": st.column_config.TextColumn(width="large"),
            }
        )

        # Add scenario calculation info
        st.divider()
        st.markdown("**Fórmula de Disponibilidade:**")
        st.latex(r"D_{final} = FC \times (1 - FCp) \times FS \times FL \times 100\%")
        st.caption(
            f"Cenário: {scenario} | "
            f"Disponibilidade Final: {residue_data.availability.final_availability:.1f}%"
        )
    else:
        st.info("Sem dados de fatores de disponibilidade")


def _render_sub_residues_summary(residue_data: ResidueData, scenario: str) -> None:
    """Render summary of sub-residues in compact format."""
    from src.services import ContributionAnalyzer

    if not residue_data.sub_residues:
        return

    # Calculate contributions
    contributions = ContributionAnalyzer.calculate_contributions(
        residue_data.sub_residues,
        scenario
    )

    # Display as metrics
    cols = st.columns(len(contributions))
    for col, contrib in zip(cols, contributions):
        with col:
            ch4 = contrib['ch4']
            pct = contrib['percentage']
            st.metric(
                f"{contrib['icon']} {contrib['name'][:15]}",
                f"{pct:.1f}%",
                f"{format_biogas_potential(ch4)}"
            )

    # Detailed table
    st.markdown("**Detalhes por Sub-Resíduo:**")
    import pandas as pd

    detail_data = []
    for contrib in contributions:
        if contrib['ch4'] > 0 or contrib['name'] == contributions[0]['name']:  # Always show first
            detail_data.append({
                "Sub-Resíduo": contrib['name'],
                "CH₄ Potencial": format_biogas_potential(contrib['ch4']),
                "% do Total": f"{contrib['percentage']:.1f}%",
                "Posição": f"#{contrib['rank']}"
            })

    if detail_data:
        df = pd.DataFrame(detail_data)
        st.dataframe(df, width="stretch", hide_index=True)


def _render_references(references: list) -> None:
    """Render scientific references in collapsible format."""
    for i, ref in enumerate(references[:5], 1):  # Show first 5
        with st.expander(f"{i}. {ref.title[:60]}...", expanded=False):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**Autores:** {ref.authors}")
                st.markdown(f"**Ano:** {ref.year}")
                if ref.journal:
                    st.markdown(f"**Periódico:** {ref.journal}")
                if ref.doi:
                    st.markdown(f"**DOI:** [{ref.doi}](https://doi.org/{ref.doi})")

            with col2:
                relevance_color = "green" if ref.relevance == "Very High" else "blue" if ref.relevance == "High" else "gray"
                st.markdown(f":{relevance_color}[**{ref.relevance}**]")

            if ref.key_findings:
                st.markdown("**Principais Achados:**")
                for finding in ref.key_findings[:2]:  # Show first 2 findings
                    st.caption(f"• {finding[:100]}")

    if len(references) > 5:
        st.caption(f"... e mais {len(references) - 5} referências")


def render_sub_residue_card(
    sub_residue: ResidueData,
    parent_name: str = "",
    scenario: str = 'Realista'
) -> None:
    """
    Render compact card for a sub-residue within a parent residue.

    Args:
        sub_residue: Sub-residue ResidueData object
        parent_name: Name of parent residue (for context)
        scenario: Which scenario to display

    Returns:
        None (renders to Streamlit)
    """
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 8, 2])

        with col1:
            st.markdown(f"## {sub_residue.icon}")

        with col2:
            st.markdown(f"**{sub_residue.name}**")
            if parent_name:
                st.caption(f"Componente de: {parent_name}")

        with col3:
            availability_pct = sub_residue.availability.final_availability
            st.metric("Disponibilidade", f"{availability_pct:.1f}%")

        st.divider()

        col1, col2, col3 = st.columns(3)
        with col1:
            ch4 = sub_residue.scenarios.get(scenario, 0.0)
            st.metric("CH₄ Potencial", format_biogas_potential(ch4))
        with col2:
            st.metric("Umidade", f"{sub_residue.chemical_params.moisture:.1f}%")
        with col3:
            st.metric("BMP", f"{sub_residue.chemical_params.bmp} {sub_residue.chemical_params.bmp_unit.split('|')[0]}")

        # Compact factors display
        with st.expander("Fatores (FC/FCp/FS/FL)"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("FC", f"{sub_residue.availability.fc:.2f}")
            with col2:
                st.metric("FCp", f"{sub_residue.availability.fcp:.2f}")
            with col3:
                st.metric("FS", f"{sub_residue.availability.fs:.2f}")
            with col4:
                st.metric("FL", f"{sub_residue.availability.fl:.2f}")
