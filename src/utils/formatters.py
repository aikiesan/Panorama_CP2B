"""
Formatters Utility - Data Formatting Functions
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Common formatting functions for numbers, units, and ranges.
"""

from typing import Optional, Union


def format_number(
    value: Union[int, float],
    decimals: int = 2,
    thousands_sep: str = ",",
    decimal_sep: str = "."
) -> str:
    """
    Format number with thousands separator.

    Args:
        value: Number to format
        decimals: Number of decimal places
        thousands_sep: Thousands separator character
        decimal_sep: Decimal separator character

    Returns:
        Formatted number string
    """
    if value is None:
        return "N/A"

    # Format with decimals
    formatted = f"{value:,.{decimals}f}"

    # Replace separators if needed
    if thousands_sep != ",":
        formatted = formatted.replace(",", "TEMP")
        formatted = formatted.replace(".", ",")
        formatted = formatted.replace("TEMP", thousands_sep)

    return formatted


def format_range(
    min_val: Optional[float],
    mean_val: Optional[float],
    max_val: Optional[float],
    unit: str = "",
    decimals: int = 1
) -> str:
    """
    Format range as "min - mean - max unit" or variations.

    Args:
        min_val: Minimum value
        mean_val: Mean/current value
        max_val: Maximum value
        unit: Unit of measurement
        decimals: Number of decimal places

    Returns:
        Formatted range string
    """
    unit_str = f" {unit}" if unit else ""

    if min_val is not None and max_val is not None and mean_val is not None:
        return f"{min_val:.{decimals}f} - {mean_val:.{decimals}f} - {max_val:.{decimals}f}{unit_str}"
    elif min_val is not None and max_val is not None:
        return f"{min_val:.{decimals}f} - {max_val:.{decimals}f}{unit_str}"
    elif mean_val is not None:
        return f"{mean_val:.{decimals}f}{unit_str}"
    else:
        return "N/A"


def format_unit(value: float, unit: str, decimals: int = 2) -> str:
    """
    Format value with unit.

    Args:
        value: Numeric value
        unit: Unit string
        decimals: Number of decimal places

    Returns:
        Formatted string "value unit"
    """
    if value is None:
        return f"N/A {unit}"

    return f"{value:.{decimals}f} {unit}"


def format_percentage(value: float, decimals: int = 1, include_symbol: bool = True) -> str:
    """
    Format percentage value.

    Args:
        value: Percentage value (0-100)
        decimals: Number of decimal places
        include_symbol: Include % symbol

    Returns:
        Formatted percentage string
    """
    if value is None:
        return "N/A"

    formatted = f"{value:.{decimals}f}"
    if include_symbol:
        formatted += "%"

    return formatted


def format_scientific(value: float, precision: int = 2) -> str:
    """
    Format number in scientific notation.

    Args:
        value: Number to format
        precision: Number of significant figures

    Returns:
        Scientific notation string
    """
    if value is None:
        return "N/A"

    return f"{value:.{precision}e}"


def format_biogas_potential(ch4_m3_ano: float, include_unit: bool = True) -> str:
    """
    Format biogas potential with appropriate scale (Mi, Bi, etc.).

    Args:
        ch4_m3_ano: CH4 potential in m³/year
        include_unit: Include unit string

    Returns:
        Formatted potential string
    """
    if ch4_m3_ano is None or ch4_m3_ano == 0:
        return "N/A"

    # Determine scale
    if ch4_m3_ano >= 1_000_000_000:  # Billion
        value = ch4_m3_ano / 1_000_000_000
        unit = "Bi m³/ano" if include_unit else ""
        return f"{value:.2f} {unit}".strip()
    elif ch4_m3_ano >= 1_000_000:  # Million
        value = ch4_m3_ano / 1_000_000
        unit = "Mi m³/ano" if include_unit else ""
        return f"{value:.2f} {unit}".strip()
    elif ch4_m3_ano >= 1_000:  # Thousand
        value = ch4_m3_ano / 1_000
        unit = "mil m³/ano" if include_unit else ""
        return f"{value:.2f} {unit}".strip()
    else:
        unit = "m³/ano" if include_unit else ""
        return f"{ch4_m3_ano:.0f} {unit}".strip()


def format_electricity_potential(ch4_m3_ano: float, conversion_factor: float = 1.43) -> str:
    """
    Convert CH4 potential to electricity equivalent.

    Args:
        ch4_m3_ano: CH4 potential in m³/year
        conversion_factor: Conversion factor (kWh/m³ CH4), default 1.43

    Returns:
        Formatted electricity potential string
    """
    if ch4_m3_ano is None or ch4_m3_ano == 0:
        return "N/A"

    # Calculate GWh
    gwh_ano = (ch4_m3_ano * conversion_factor) / 1_000_000

    if gwh_ano >= 1_000:  # TWh
        return f"{gwh_ano/1000:.2f} TWh/ano"
    else:
        return f"{gwh_ano:.2f} GWh/ano"


__all__ = [
    'format_number',
    'format_range',
    'format_unit',
    'format_percentage',
    'format_scientific',
    'format_biogas_potential',
    'format_electricity_potential'
]
