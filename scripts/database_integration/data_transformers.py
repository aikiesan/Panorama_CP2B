"""
Data Transformers Module - Single Responsibility Principle

Transforms validated data into database schema format.
Each function performs ONE specific transformation.
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_residue_name_mapping(mapping_file: Optional[str] = None) -> Dict[str, str]:
    """
    Load residue name mapping from JSON file.

    Args:
        mapping_file: Path to mapping JSON file. If None, returns empty dict.

    Returns:
        Dict[str, str]: Mapping from code to standard name
    """
    if mapping_file is None:
        return {}

    path = Path(mapping_file)
    if not path.exists():
        logger.warning(f"Mapping file not found: {mapping_file}")
        return {}

    with open(path, 'r', encoding='utf-8') as f:
        mapping = json.load(f)

    logger.info(f"Loaded {len(mapping)} residue name mappings")
    return mapping


def normalize_residue_names(df: pd.DataFrame, mapping: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Normalize residue names using provided mapping.

    Args:
        df: DataFrame with 'codigo' and/or 'nome' columns
        mapping: Dictionary mapping codes to standard names

    Returns:
        pd.DataFrame: DataFrame with normalized names
    """
    logger.info("Normalizing residue names...")

    df_normalized = df.copy()

    if mapping and 'codigo' in df.columns:
        # Apply mapping to names based on codes
        if 'nome' in df.columns:
            df_normalized['nome'] = df_normalized['codigo'].map(
                lambda x: mapping.get(x, df_normalized.loc[df_normalized['codigo'] == x, 'nome'].iloc[0]
                                       if x in df_normalized['codigo'].values else x)
            )
            logger.info(f"Applied name mapping to {len(df_normalized)} residues")

    return df_normalized


def transform_scenario_to_municipalities(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform scenario data to match municipalities table schema.

    Args:
        df: DataFrame from POTENCIAL_3CENARIOS_VALIDADO

    Returns:
        pd.DataFrame: Transformed data ready for database insertion
    """
    logger.info("Transforming scenario data for municipalities table...")

    df_transformed = df.copy()

    # Rename columns to match database schema (adding scenario prefix)
    column_mapping = {
        # Pessimistic scenario
        'ch4_pes_agricultura': 'ch4_pessimistic_agricultura',
        'ch4_pes_pecuaria': 'ch4_pessimistic_pecuaria',
        'ch4_pes_urbano': 'ch4_pessimistic_urbano',
        'ch4_pes_total': 'ch4_pessimistic_total',
        'energia_pes_mwh': 'energia_pessimistic_mwh',
        'energia_pes_tj': 'energia_pessimistic_tj',

        # Realistic scenario
        'ch4_rea_agricultura': 'ch4_realistic_agricultura',
        'ch4_rea_pecuaria': 'ch4_realistic_pecuaria',
        'ch4_rea_urbano': 'ch4_realistic_urbano',
        'ch4_rea_total': 'ch4_realistic_total',
        'energia_rea_mwh': 'energia_realistic_mwh',
        'energia_rea_tj': 'energia_realistic_tj',

        # Optimistic scenario
        'ch4_oti_agricultura': 'ch4_optimistic_agricultura',
        'ch4_oti_pecuaria': 'ch4_optimistic_pecuaria',
        'ch4_oti_urbano': 'ch4_optimistic_urbano',
        'ch4_oti_total': 'ch4_optimistic_total',
        'energia_oti_mwh': 'energia_optimistic_mwh',
        'energia_oti_tj': 'energia_optimistic_tj',

        # Theoretical
        'ch4_teorico': 'ch4_theoretical'
    }

    # Only rename columns that exist
    existing_mapping = {k: v for k, v in column_mapping.items() if k in df_transformed.columns}
    df_transformed = df_transformed.rename(columns=existing_mapping)

    logger.info(f"Transformed {len(df_transformed)} municipalities with scenario data")
    logger.info(f"Added columns: {list(existing_mapping.values())}")

    return df_transformed


def transform_factors_to_residues(df: pd.DataFrame, sector_map: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Transform availability factors data for residue tables.

    Args:
        df: DataFrame from FATORES_DISPONIBILIDADE_COMPLETOS
        sector_map: Optional mapping from sector codes to full names

    Returns:
        pd.DataFrame: Transformed data ready for database insertion
    """
    logger.info("Transforming availability factors for residue tables...")

    df_transformed = df.copy()

    # Default sector mapping if not provided
    if sector_map is None:
        sector_map = {
            'AG_AGRICULTURA': 'Agrícola',
            'PC_PECUARIA': 'Pecuária',
            'UR_URBANO': 'Urbano',
            'IN_INDUSTRIAL': 'Industrial'
        }

    # Map sector codes to names
    if 'setor' in df_transformed.columns:
        df_transformed['setor_nome'] = df_transformed['setor'].map(
            lambda x: sector_map.get(x, x)
        )

    # Ensure all SAF factors are properly formatted
    saf_columns = ['fc_medio', 'fcp_medio', 'fs_medio', 'fl_medio', 'fator_total']
    for col in saf_columns:
        if col in df_transformed.columns:
            df_transformed[col] = pd.to_numeric(df_transformed[col], errors='coerce')

    # Ensure BMP is numeric
    if 'bmp_medio' in df_transformed.columns:
        df_transformed['bmp_medio'] = pd.to_numeric(df_transformed['bmp_medio'], errors='coerce')

    logger.info(f"Transformed {len(df_transformed)} residues with availability factors")

    return df_transformed


def split_by_sector(df: pd.DataFrame, sector_column: str = 'setor_nome') -> Dict[str, pd.DataFrame]:
    """
    Split residues DataFrame by sector for inserting into sector-specific tables.

    Args:
        df: DataFrame with residue data
        sector_column: Column name containing sector information

    Returns:
        Dict[str, pd.DataFrame]: Dictionary with keys as sector names and values as filtered DataFrames
    """
    logger.info("Splitting residues by sector...")

    if sector_column not in df.columns:
        logger.warning(f"Sector column '{sector_column}' not found. Returning empty dict.")
        return {}

    sectors = {
        'Agrícola': 'residuos_agricolas',
        'Pecuária': 'residuos_pecuarios',
        'Urbano': 'residuos_urbanos',
        'Industrial': 'residuos_industriais'
    }

    sector_dfs = {}

    for sector_name, table_name in sectors.items():
        sector_df = df[df[sector_column] == sector_name].copy()
        if len(sector_df) > 0:
            sector_dfs[table_name] = sector_df
            logger.info(f"  {sector_name}: {len(sector_df)} residues -> {table_name}")

    return sector_dfs


def prepare_scenario_update_query(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare scenario data for UPDATE query (not INSERT).

    Args:
        df: Transformed scenario DataFrame

    Returns:
        pd.DataFrame: DataFrame with only update-relevant columns
    """
    logger.info("Preparing scenario data for UPDATE operation...")

    # Keep municipality identifier and all scenario columns
    keep_cols = ['codigo_municipio']

    # Add all scenario-related columns
    scenario_prefixes = ['ch4_pessimistic', 'ch4_realistic', 'ch4_optimistic',
                         'energia_pessimistic', 'energia_realistic', 'energia_optimistic',
                         'ch4_theoretical']

    for col in df.columns:
        if any(col.startswith(prefix) for prefix in scenario_prefixes):
            keep_cols.append(col)

    df_update = df[[col for col in keep_cols if col in df.columns]].copy()

    logger.info(f"Prepared {len(df_update)} rows for scenario update with {len(df_update.columns)} columns")

    return df_update


def calculate_sector_totals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate sector totals from scenario breakdowns.

    Args:
        df: DataFrame with sector-specific scenario columns

    Returns:
        pd.DataFrame: DataFrame with added total columns
    """
    logger.info("Calculating sector totals...")

    df_calc = df.copy()

    # For each scenario, calculate total from sectors
    scenarios = ['pessimistic', 'realistic', 'optimistic']

    for scenario in scenarios:
        agr_col = f'ch4_{scenario}_agricultura'
        pec_col = f'ch4_{scenario}_pecuaria'
        urb_col = f'ch4_{scenario}_urbano'
        total_col = f'ch4_{scenario}_total'

        if all(col in df_calc.columns for col in [agr_col, pec_col, urb_col]):
            # Calculate total (sum of sectors)
            df_calc[total_col] = (
                df_calc[agr_col].fillna(0) +
                df_calc[pec_col].fillna(0) +
                df_calc[urb_col].fillna(0)
            )
            logger.info(f"Calculated {total_col} from sector columns")

    return df_calc
