"""
Data Validators Module - Single Responsibility Principle

Validates data quality, integrity, and consistency.
Each function performs ONE specific validation check.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_municipality_codes(df: pd.DataFrame, reference_codes: Optional[List[int]] = None) -> Tuple[bool, Dict]:
    """
    Validate municipality codes against reference list.

    Args:
        df: DataFrame with 'codigo_municipio' column
        reference_codes: Optional list of valid municipality codes

    Returns:
        Tuple[bool, Dict]: (is_valid, validation_report)
            validation_report contains: matched_count, total_count, unmatched_codes
    """
    logger.info("Validating municipality codes...")

    if 'codigo_municipio' not in df.columns:
        return False, {'error': 'Missing codigo_municipio column'}

    codes = df['codigo_municipio'].unique()
    total_count = len(codes)

    if reference_codes is None:
        # No reference to compare against
        return True, {
            'total_count': total_count,
            'message': 'No reference codes provided - skipping validation'
        }

    matched = set(codes) & set(reference_codes)
    unmatched = set(codes) - set(reference_codes)

    matched_count = len(matched)
    match_rate = (matched_count / total_count * 100) if total_count > 0 else 0

    is_valid = match_rate >= 95  # 95% threshold

    report = {
        'matched_count': matched_count,
        'total_count': total_count,
        'match_rate': match_rate,
        'unmatched_codes': list(unmatched),
        'is_valid': is_valid
    }

    if is_valid:
        logger.info(f"Municipality code validation PASSED: {match_rate:.1f}% match")
    else:
        logger.warning(f"Municipality code validation FAILED: {match_rate:.1f}% match")

    return is_valid, report


def validate_saf_factors(df: pd.DataFrame) -> Tuple[bool, Dict]:
    """
    Validate SAF (Sustainability Availability Factor) values are in valid range [0, 1].

    Args:
        df: DataFrame with SAF factor columns (fc_medio, fcp_medio, fs_medio, fl_medio)

    Returns:
        Tuple[bool, Dict]: (is_valid, validation_report)
    """
    logger.info("Validating SAF factors...")

    factor_cols = ['fc_medio', 'fcp_medio', 'fs_medio', 'fl_medio']
    available_cols = [col for col in factor_cols if col in df.columns]

    if not available_cols:
        return True, {'message': 'No SAF factor columns found - skipping validation'}

    invalid_rows = []

    for col in available_cols:
        # Skip NaN values in validation
        non_null = df[col].notna()
        invalid = non_null & ((df[col] < 0) | (df[col] > 1))

        if invalid.any():
            invalid_indices = df[invalid].index.tolist()
            invalid_rows.append({
                'column': col,
                'invalid_count': len(invalid_indices),
                'invalid_indices': invalid_indices[:5]  # Show first 5
            })

    is_valid = len(invalid_rows) == 0

    report = {
        'is_valid': is_valid,
        'checked_columns': available_cols,
        'invalid_rows': invalid_rows
    }

    if is_valid:
        logger.info("SAF factor validation PASSED")
    else:
        logger.warning(f"SAF factor validation FAILED: {len(invalid_rows)} columns with invalid values")

    return is_valid, report


def validate_numeric_columns(df: pd.DataFrame, columns: List[str]) -> Tuple[bool, Dict]:
    """
    Validate that specified columns contain numeric data and no invalid values.

    Args:
        df: DataFrame to validate
        columns: List of column names that should be numeric

    Returns:
        Tuple[bool, Dict]: (is_valid, validation_report)
    """
    logger.info(f"Validating numeric columns: {columns}")

    missing_cols = [col for col in columns if col not in df.columns]

    if missing_cols:
        return False, {
            'error': f'Missing columns: {missing_cols}',
            'is_valid': False
        }

    non_numeric = []
    has_inf = []
    all_null = []

    for col in columns:
        # Check if numeric
        if not pd.api.types.is_numeric_dtype(df[col]):
            non_numeric.append(col)

        # Check for infinity
        if pd.api.types.is_numeric_dtype(df[col]) and np.isinf(df[col]).any():
            has_inf.append(col)

        # Check for all null
        if df[col].isna().all():
            all_null.append(col)

    is_valid = len(non_numeric) == 0 and len(has_inf) == 0

    report = {
        'is_valid': is_valid,
        'total_columns': len(columns),
        'non_numeric': non_numeric,
        'has_infinity': has_inf,
        'all_null': all_null
    }

    if is_valid:
        logger.info("Numeric column validation PASSED")
    else:
        logger.warning(f"Numeric column validation FAILED")

    return is_valid, report


def validate_required_columns(df: pd.DataFrame, required: List[str]) -> Tuple[bool, Dict]:
    """
    Validate that all required columns are present in DataFrame.

    Args:
        df: DataFrame to validate
        required: List of required column names

    Returns:
        Tuple[bool, Dict]: (is_valid, validation_report)
    """
    logger.info(f"Validating required columns...")

    missing = [col for col in required if col not in df.columns]
    is_valid = len(missing) == 0

    report = {
        'is_valid': is_valid,
        'required_count': len(required),
        'missing_columns': missing,
        'present_columns': [col for col in required if col in df.columns]
    }

    if is_valid:
        logger.info("Required columns validation PASSED")
    else:
        logger.warning(f"Required columns validation FAILED: missing {missing}")

    return is_valid, report


def validate_no_duplicates(df: pd.DataFrame, subset: List[str]) -> Tuple[bool, Dict]:
    """
    Validate that there are no duplicate rows based on subset of columns.

    Args:
        df: DataFrame to validate
        subset: List of columns to check for duplicates

    Returns:
        Tuple[bool, Dict]: (is_valid, validation_report)
    """
    logger.info(f"Validating no duplicates on: {subset}")

    duplicates = df.duplicated(subset=subset, keep=False)
    duplicate_count = duplicates.sum()
    is_valid = duplicate_count == 0

    report = {
        'is_valid': is_valid,
        'duplicate_count': duplicate_count,
        'total_rows': len(df)
    }

    if is_valid:
        logger.info("Duplicate validation PASSED")
    else:
        logger.warning(f"Duplicate validation FAILED: {duplicate_count} duplicate rows found")

    return is_valid, report


def validate_positive_values(df: pd.DataFrame, columns: List[str]) -> Tuple[bool, Dict]:
    """
    Validate that specified columns contain only non-negative values.

    Args:
        df: DataFrame to validate
        columns: List of columns that should have non-negative values

    Returns:
        Tuple[bool, Dict]: (is_valid, validation_report)
    """
    logger.info(f"Validating positive values for: {columns}")

    negative_cols = []

    for col in columns:
        if col not in df.columns:
            continue

        # Skip NaN values
        non_null = df[col].notna()
        has_negative = (df[col][non_null] < 0).any()

        if has_negative:
            negative_count = (df[col][non_null] < 0).sum()
            negative_cols.append({
                'column': col,
                'negative_count': negative_count
            })

    is_valid = len(negative_cols) == 0

    report = {
        'is_valid': is_valid,
        'checked_columns': columns,
        'negative_columns': negative_cols
    }

    if is_valid:
        logger.info("Positive values validation PASSED")
    else:
        logger.warning(f"Positive values validation FAILED: {len(negative_cols)} columns with negative values")

    return is_valid, report


def generate_validation_report(df: pd.DataFrame, data_type: str) -> Dict:
    """
    Generate comprehensive validation report for a DataFrame.

    Args:
        df: DataFrame to validate
        data_type: Type of data ('scenarios', 'factors', 'complete_potential')

    Returns:
        Dict: Comprehensive validation report with all checks
    """
    logger.info(f"Generating validation report for: {data_type}")

    report = {
        'data_type': data_type,
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns),
        'validations': {}
    }

    # Scenario-specific validations
    if data_type == 'scenarios':
        required = ['codigo_municipio', 'nome_municipio', 'ch4_pes_total',
                    'ch4_rea_total', 'ch4_oti_total']
        valid, result = validate_required_columns(df, required)
        report['validations']['required_columns'] = result

        if valid:
            numeric_cols = ['ch4_pes_total', 'ch4_rea_total', 'ch4_oti_total',
                            'energia_pes_mwh', 'energia_rea_mwh', 'energia_oti_mwh']
            numeric_cols = [c for c in numeric_cols if c in df.columns]
            valid, result = validate_numeric_columns(df, numeric_cols)
            report['validations']['numeric_columns'] = result

            valid, result = validate_positive_values(df, numeric_cols)
            report['validations']['positive_values'] = result

            valid, result = validate_no_duplicates(df, ['codigo_municipio'])
            report['validations']['no_duplicates'] = result

    # Factors-specific validations
    elif data_type == 'factors':
        required = ['codigo', 'nome', 'setor', 'bmp_medio']
        valid, result = validate_required_columns(df, required)
        report['validations']['required_columns'] = result

        if valid:
            valid, result = validate_saf_factors(df)
            report['validations']['saf_factors'] = result

            valid, result = validate_no_duplicates(df, ['codigo'])
            report['validations']['no_duplicates'] = result

    # Summary
    all_valid = all(
        v.get('is_valid', False) for v in report['validations'].values()
    )
    report['overall_valid'] = all_valid

    if all_valid:
        logger.info(f"Validation report for {data_type}: PASSED")
    else:
        logger.warning(f"Validation report for {data_type}: FAILED")

    return report
