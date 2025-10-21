"""
Data Loaders Module - Single Responsibility Principle

Handles loading data from CSV/Excel files and Jupyter notebooks.
Each function loads ONE specific data source.
"""

import pandas as pd
from pathlib import Path
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_scenario_data(file_path: str) -> pd.DataFrame:
    """
    Load municipality scenario data from validated CSV/Excel file.

    Args:
        file_path: Path to POTENCIAL_3CENARIOS_VALIDADO file (.csv or .xlsx)

    Returns:
        pd.DataFrame: Municipality data with 3 scenarios (pessimistic, realistic, optimistic)

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If required columns are missing
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Scenario data file not found: {file_path}")

    logger.info(f"Loading scenario data from: {path.name}")

    # Load based on file extension
    if path.suffix == '.csv':
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    elif path.suffix == '.xlsx':
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}. Use .csv or .xlsx")

    # Validate required columns
    required_cols = ['codigo_municipio', 'nome_municipio', 'ch4_pes_total',
                     'ch4_rea_total', 'ch4_oti_total']
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    logger.info(f"Loaded {len(df)} municipalities with scenario data")
    return df


def load_availability_factors(file_path: str) -> pd.DataFrame:
    """
    Load residue availability factors (SAF) from validated CSV file.

    Args:
        file_path: Path to FATORES_DISPONIBILIDADE_COMPLETOS.csv

    Returns:
        pd.DataFrame: Residue data with BMP and SAF factors (FC, FCp, FS, FL)

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If required columns are missing
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Availability factors file not found: {file_path}")

    logger.info(f"Loading availability factors from: {path.name}")

    # Load CSV with UTF-8 BOM handling
    df = pd.read_csv(file_path, encoding='utf-8-sig')

    # Validate required columns
    required_cols = ['codigo', 'nome', 'setor', 'bmp_medio']
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    logger.info(f"Loaded {len(df)} residues with availability factors")
    return df


def load_complete_potential_data(file_path: str) -> pd.DataFrame:
    """
    Load complete SP state potential data with all residue breakdowns.

    Args:
        file_path: Path to POTENCIAL_COMPLETO_SP file (.csv or .xlsx)

    Returns:
        pd.DataFrame: Complete potential data by municipality and residue

    Raises:
        FileNotFoundError: If file does not exist
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Complete potential file not found: {file_path}")

    logger.info(f"Loading complete potential data from: {path.name}")

    # Load based on file extension
    if path.suffix == '.csv':
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    elif path.suffix == '.xlsx':
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")

    logger.info(f"Loaded {len(df)} rows of complete potential data")
    return df


def load_all_factors(file_path: str) -> pd.DataFrame:
    """
    Load complete factor calculations for all residues.

    Args:
        file_path: Path to FATORES_COMPLETOS_TODOS.csv

    Returns:
        pd.DataFrame: Complete factor calculations

    Raises:
        FileNotFoundError: If file does not exist
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Complete factors file not found: {file_path}")

    logger.info(f"Loading complete factors from: {path.name}")

    df = pd.read_csv(file_path, encoding='utf-8-sig')

    logger.info(f"Loaded {len(df)} rows of complete factor data")
    return df


def discover_validation_files(base_dir: str) -> dict:
    """
    Discover and return paths to all validation data files.

    Args:
        base_dir: Base directory for validated data (e.g., C:\\Users\\Lucas\\Documents\\CP2B\\Validacao_dados)

    Returns:
        dict: Dictionary with keys 'scenarios', 'factors', 'complete_potential', 'all_factors'
              and values as file paths

    Raises:
        FileNotFoundError: If base directory or required files not found
    """
    base_path = Path(base_dir)

    if not base_path.exists():
        raise FileNotFoundError(f"Base validation directory not found: {base_dir}")

    logger.info(f"Discovering validation files in: {base_dir}")

    files = {
        'scenarios': None,
        'factors': None,
        'complete_potential': None,
        'all_factors': None
    }

    # Look for scenario data (06_RESULTADO_FINAL_VALIDADO)
    final_validado = base_path / "06_RESULTADO_FINAL_VALIDADO"
    if final_validado.exists():
        scenario_files = list(final_validado.glob("POTENCIAL_3CENARIOS_VALIDADO*.csv"))
        if scenario_files:
            files['scenarios'] = str(scenario_files[0])
            logger.info(f"Found scenarios: {scenario_files[0].name}")

    # Look for factors (05_RESULTADO_FINAL)
    final_resultado = base_path / "05_RESULTADO_FINAL"
    if final_resultado.exists():
        # Availability factors
        factor_files = list(final_resultado.glob("FATORES_DISPONIBILIDADE_COMPLETOS.csv"))
        if factor_files:
            files['factors'] = str(factor_files[0])
            logger.info(f"Found factors: {factor_files[0].name}")

        # Complete potential
        potential_files = list(final_resultado.glob("POTENCIAL_COMPLETO_SP*.csv"))
        if potential_files:
            files['complete_potential'] = str(potential_files[0])
            logger.info(f"Found complete potential: {potential_files[0].name}")

        # All factors
        all_factor_files = list(final_resultado.glob("FATORES_COMPLETOS_TODOS.csv"))
        if all_factor_files:
            files['all_factors'] = str(all_factor_files[0])
            logger.info(f"Found all factors: {all_factor_files[0].name}")

    # Check if we found the essential files
    missing = [k for k, v in files.items() if v is None and k in ['scenarios', 'factors']]
    if missing:
        logger.warning(f"Missing essential files: {missing}")

    return files


def get_validation_base_dir() -> str:
    """
    Get the default validation data base directory.

    Returns:
        str: Default path to validation data folder
    """
    return r"C:\Users\Lucas\Documents\CP2B\Validacao_dados"
