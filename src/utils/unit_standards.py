"""
Unit Standards Module
Provides standardized unit display for chemical parameters based on CP2B guidelines.

Loads unit mapping from CP2B_Unit_Standards_Reference.csv and provides
helper functions to get standard units for each parameter/residue combination.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional


# Path to unit standards CSV
UNIT_STANDARDS_PATH = Path(r"C:\Users\Lucas\Downloads\CP2B_Unit_Standards_Reference.csv")


# Cache for unit standards data
_UNIT_STANDARDS_CACHE = None


def load_unit_standards() -> pd.DataFrame:
    """
    Load CP2B unit standards from CSV file.

    Returns:
        pd.DataFrame: Unit standards with columns for each residue type

    Raises:
        FileNotFoundError: If CSV file doesn't exist
    """
    global _UNIT_STANDARDS_CACHE

    if _UNIT_STANDARDS_CACHE is not None:
        return _UNIT_STANDARDS_CACHE

    if not UNIT_STANDARDS_PATH.exists():
        raise FileNotFoundError(
            f"Unit standards file not found: {UNIT_STANDARDS_PATH}\n"
            "Please ensure CP2B_Unit_Standards_Reference.csv is in Downloads folder."
        )

    df = pd.read_csv(UNIT_STANDARDS_PATH)
    _UNIT_STANDARDS_CACHE = df

    return df


def get_standard_unit(parameter_code: str, residue_type: str = "vinhaça") -> str:
    """
    Get standard display unit for a parameter based on residue type.

    Args:
        parameter_code: Parameter code (e.g., 'BMP', 'TS', 'COD', 'pH')
        residue_type: Type of residue - 'vinhaça', 'bagaço', 'palha', 'torta'
                      (defaults to 'vinhaça' for liquid residues)

    Returns:
        str: Standard unit (e.g., 'mL CH₄/g VS', 'g/L', '% DW', 'unitless')
             Returns 'N/A' if parameter not found

    Examples:
        >>> get_standard_unit('BMP', 'vinhaça')
        'mL CH₄/g VS'
        >>> get_standard_unit('TS', 'vinhaça')
        'g/L'
        >>> get_standard_unit('TS', 'bagaço')
        '% DW'
        >>> get_standard_unit('pH', 'vinhaça')
        'unitless'
    """
    try:
        df = load_unit_standards()

        # Find parameter row
        param_row = df[df['parameter'] == parameter_code]

        if param_row.empty:
            # Parameter not found - return N/A
            return 'N/A'

        # Determine column name based on residue type
        residue_lower = residue_type.lower()

        if 'vinhaça' in residue_lower or 'vinhaca' in residue_lower:
            col = 'vinhaça_standard'
        elif 'bagaço' in residue_lower or 'bagaco' in residue_lower:
            col = 'bagaço_standard'
        elif 'palha' in residue_lower:
            col = 'palha_standard'
        elif 'torta' in residue_lower:
            col = 'torta_standard'
        else:
            # Default to vinhaça for unknown types (liquids)
            col = 'vinhaça_standard'

        # Get standard unit
        standard_unit = param_row.iloc[0][col]

        # Handle NaN or empty values
        if pd.isna(standard_unit) or str(standard_unit).strip() == '':
            return 'N/A'

        return str(standard_unit)

    except Exception as e:
        # Fallback - return N/A if any error
        print(f"Warning: Could not load standard unit for {parameter_code}: {e}")
        return 'N/A'


def get_parameter_full_name(parameter_code: str) -> str:
    """
    Get full display name for a parameter.

    Args:
        parameter_code: Parameter code (e.g., 'BMP', 'TS')

    Returns:
        str: Full parameter name (e.g., 'Biochemical Methane Potential')

    Examples:
        >>> get_parameter_full_name('BMP')
        'Biochemical Methane Potential'
        >>> get_parameter_full_name('TS')
        'Total Solids / Dry Matter'
    """
    try:
        df = load_unit_standards()
        param_row = df[df['parameter'] == parameter_code]

        if param_row.empty:
            return parameter_code  # Return code if not found

        return str(param_row.iloc[0]['parameter_full_name'])

    except Exception:
        return parameter_code


def get_typical_range(parameter_code: str, residue_type: str = "vinhaça") -> str:
    """
    Get typical value range for a parameter.

    Args:
        parameter_code: Parameter code (e.g., 'BMP', 'TS')
        residue_type: Type of residue (used to extract range from multi-residue field)

    Returns:
        str: Typical range string (e.g., '100-400', '20-80 g/L')

    Examples:
        >>> get_typical_range('BMP', 'vinhaça')
        '100-400'
        >>> get_typical_range('TS', 'vinhaça')
        '20-80 g/L'
    """
    try:
        df = load_unit_standards()
        param_row = df[df['parameter'] == parameter_code]

        if param_row.empty:
            return 'N/A'

        range_str = str(param_row.iloc[0]['typical_range'])

        # Parse range string to extract residue-specific range
        # Format: "Vinhaça:100-400; Bagaço:150-300; ..."
        residue_lower = residue_type.lower()

        for part in range_str.split(';'):
            part = part.strip()
            if ':' in part:
                residue_name, range_value = part.split(':', 1)
                if residue_lower in residue_name.lower():
                    return range_value.strip()

        # If specific residue not found, return full range string
        return range_str

    except Exception:
        return 'N/A'


def infer_residue_type_from_name(residue_name: str) -> str:
    """
    Infer residue type category from residue name.

    Args:
        residue_name: Name of residue (e.g., 'Vinhaça', 'Bagaço de Cana')

    Returns:
        str: Residue type - 'vinhaça', 'bagaço', 'palha', or 'torta'

    Examples:
        >>> infer_residue_type_from_name('Vinhaça')
        'vinhaça'
        >>> infer_residue_type_from_name('Bagaço de Cana')
        'bagaço'
        >>> infer_residue_type_from_name('Palha de Cana')
        'palha'
    """
    name_lower = residue_name.lower()

    if 'vinhaça' in name_lower or 'vinhaca' in name_lower:
        return 'vinhaça'
    elif 'bagaço' in name_lower or 'bagaco' in name_lower:
        return 'bagaço'
    elif 'palha' in name_lower:
        return 'palha'
    elif 'torta' in name_lower or 'filter cake' in name_lower:
        return 'torta'
    else:
        # Default to liquid (vinhaça) for unknown
        return 'vinhaça'


# Parameter display configuration
PARAMETER_DISPLAY_CONFIG = {
    # Biogas Production Parameters
    'BMP': {
        'category': 'Produção de Biogás',
        'display_name': 'BMP',
        'full_name': 'Biochemical Methane Potential',
        'priority': 1
    },
    'METHANE_CONTENT': {
        'category': 'Produção de Biogás',
        'display_name': 'CH₄ Content',
        'full_name': 'Methane percentage in biogas',
        'priority': 2
    },

    # Organic Matter Indicators
    'TS': {
        'category': 'Indicadores de Matéria Orgânica',
        'display_name': 'TS',
        'full_name': 'Total Solids / Dry Matter',
        'priority': 3
    },
    'VS': {
        'category': 'Indicadores de Matéria Orgânica',
        'display_name': 'VS',
        'full_name': 'Volatile Solids / Organic Matter',
        'priority': 4
    },
    'COD': {
        'category': 'Indicadores de Matéria Orgânica',
        'display_name': 'COD',
        'full_name': 'Chemical Oxygen Demand',
        'priority': 5
    },

    # Chemical Properties
    'pH': {
        'category': 'Propriedades Químicas',
        'display_name': 'pH',
        'full_name': 'pH (acidity/alkalinity)',
        'priority': 6
    },
    'CN_RATIO': {
        'category': 'Propriedades Químicas',
        'display_name': 'C:N',
        'full_name': 'Carbon to Nitrogen Ratio',
        'priority': 7
    },
    'TAN': {
        'category': 'Propriedades Químicas',
        'display_name': 'TAN',
        'full_name': 'Total Ammoniacal Nitrogen',
        'priority': 8
    },
    'NITROGEN': {
        'category': 'Propriedades Químicas',
        'display_name': 'N',
        'full_name': 'Total Nitrogen',
        'priority': 9
    },
    'CARBON': {
        'category': 'Propriedades Químicas',
        'display_name': 'C',
        'full_name': 'Total Carbon',
        'priority': 10
    },
    'PHOSPHORUS': {
        'category': 'Propriedades Químicas',
        'display_name': 'P',
        'full_name': 'Total Phosphorus',
        'priority': 11
    },
    'POTASSIUM': {
        'category': 'Propriedades Químicas',
        'display_name': 'K',
        'full_name': 'Total Potassium',
        'priority': 12
    },

    # Structural Composition
    'PROTEIN': {
        'category': 'Composição Estrutural',
        'display_name': 'Protein',
        'full_name': 'Crude Protein',
        'priority': 13
    },
    'CELLULOSE': {
        'category': 'Composição Estrutural',
        'display_name': 'Cellulose',
        'full_name': 'Cellulose content',
        'priority': 14
    },
    'HEMICELLULOSE': {
        'category': 'Composição Estrutural',
        'display_name': 'Hemicellulose',
        'full_name': 'Hemicellulose content',
        'priority': 15
    },
    'LIGNIN': {
        'category': 'Composição Estrutural',
        'display_name': 'Lignin',
        'full_name': 'Lignin content',
        'priority': 16
    },
    'LIPIDS': {
        'category': 'Composição Estrutural',
        'display_name': 'Lipids',
        'full_name': 'Lipids / Crude Fat',
        'priority': 17
    }
}


def get_parameter_display_name(parameter_code: str) -> str:
    """Get short display name for parameter"""
    config = PARAMETER_DISPLAY_CONFIG.get(parameter_code, {})
    return config.get('display_name', parameter_code)


def get_parameter_category(parameter_code: str) -> str:
    """Get category name for parameter"""
    config = PARAMETER_DISPLAY_CONFIG.get(parameter_code, {})
    return config.get('category', 'Outros')
