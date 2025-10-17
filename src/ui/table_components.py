"""
Table Components Module - Single Responsibility Principle
Reusable table and data display components.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Optional


def render_data_table(
    df: pd.DataFrame,
    title: str = "Dados",
    columns: Optional[List[str]] = None,
    format_dict: Optional[Dict] = None,
    height: int = 400
) -> None:
    """
    Renders a formatted dataframe with download button.

    Args:
        df: DataFrame to display
        title: Title for the table section
        columns: Specific columns to display (None = all)
        format_dict: Dictionary mapping column names to format strings
        height: Height of the table in pixels
    """
    st.subheader(title)

    # Select columns if specified
    if columns:
        df_display = df[columns].copy()
    else:
        df_display = df.copy()

    # Apply formatting
    if format_dict:
        df_display = df_display.style.format(format_dict)

    # Display table
    st.dataframe(df_display, width="stretch", height=height)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Baixar dados (CSV)",
        data=csv,
        file_name=f"{title.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )


def render_parameter_ranges_table(ranges_data: List[Dict], title: str = "Parâmetros") -> None:
    """
    Renders a table showing parameter ranges (MIN/MEAN/MAX).

    Args:
        ranges_data: List of dictionaries with parameter range data
        title: Title for the table section
    """
    if not ranges_data:
        st.info("Nenhum dado de range disponível")
        return

    st.markdown(f"### {title}")

    df_ranges = pd.DataFrame(ranges_data)

    st.dataframe(
        df_ranges,
        hide_index=True,
        width="stretch",
        height=min(400, len(df_ranges) * 40 + 40)
    )

    # Download button
    csv = df_ranges.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Baixar tabela (CSV)",
        data=csv,
        file_name=f"{title.lower().replace(' ', '_')}_ranges.csv",
        mime="text/csv"
    )


def render_comparison_table(
    lab_data: Dict,
    lit_data: Dict,
    thresholds: Dict,
    title: str = "Comparação Lab vs Literatura"
) -> pd.DataFrame:
    """
    Renders a comparison table between laboratory and literature data.

    Args:
        lab_data: Dictionary with laboratory values
        lit_data: Dictionary with literature reference values (mean)
        thresholds: Dictionary with acceptable deviation thresholds (%)
        title: Title for the table section

    Returns:
        pd.DataFrame: Comparison results
    """
    st.markdown(f"### {title}")

    comparison_rows = []

    for param, lab_value in lab_data.items():
        if param not in lit_data:
            continue

        lit_value = lit_data[param]
        threshold = thresholds.get(param, 15)  # Default 15% threshold

        # Calculate deviation
        if lit_value > 0:
            deviation_pct = ((lab_value - lit_value) / lit_value) * 100
        else:
            deviation_pct = 0

        # Determine status
        if abs(deviation_pct) <= threshold:
            status = "✅ Dentro da faixa"
            status_color = "🟢"
        elif abs(deviation_pct) <= threshold * 1.5:
            status = "⚠️ Desvio aceitável"
            status_color = "🟡"
        else:
            status = "❌ Fora da faixa"
            status_color = "🔴"

        comparison_rows.append({
            "Parâmetro": param,
            "Valor Lab": f"{lab_value:.2f}",
            "Valor Literatura": f"{lit_value:.2f}",
            "Desvio (%)": f"{deviation_pct:+.1f}%",
            "Status": f"{status_color} {status}"
        })

    df_comparison = pd.DataFrame(comparison_rows)

    st.dataframe(
        df_comparison,
        hide_index=True,
        width="stretch",
        height=min(500, len(df_comparison) * 40 + 40)
    )

    # Download button
    csv = df_comparison.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Baixar comparação (CSV)",
        data=csv,
        file_name="comparacao_lab_literatura.csv",
        mime="text/csv"
    )

    return df_comparison


__all__ = [
    'render_data_table',
    'render_parameter_ranges_table',
    'render_comparison_table'
]
