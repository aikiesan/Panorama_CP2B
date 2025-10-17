"""
Validators Utility - Data Validation Functions
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Validation functions for residue data and parameters.
"""

from typing import Optional, List, Dict, Any
from src.models.residue_models import ResidueData, ParameterRange


def validate_range(
    min_val: Optional[float],
    mean_val: Optional[float],
    max_val: Optional[float]
) -> tuple[bool, Optional[str]]:
    """
    Validate that range values are consistent (min <= mean <= max).

    Args:
        min_val: Minimum value
        mean_val: Mean value
        max_val: Maximum value

    Returns:
        Tuple of (is_valid, error_message)
    """
    # If all None, it's valid (no range)
    if min_val is None and mean_val is None and max_val is None:
        return True, None

    # If mean is None but min/max exist, calculate mean
    if mean_val is None and min_val is not None and max_val is not None:
        mean_val = (min_val + max_val) / 2

    # Check consistency
    if min_val is not None and mean_val is not None:
        if min_val > mean_val:
            return False, f"Minimum value ({min_val}) is greater than mean value ({mean_val})"

    if mean_val is not None and max_val is not None:
        if mean_val > max_val:
            return False, f"Mean value ({mean_val}) is greater than maximum value ({max_val})"

    if min_val is not None and max_val is not None:
        if min_val > max_val:
            return False, f"Minimum value ({min_val}) is greater than maximum value ({max_val})"

    return True, None


def validate_parameter_range(param_range: ParameterRange) -> tuple[bool, Optional[str]]:
    """
    Validate ParameterRange object.

    Args:
        param_range: ParameterRange object to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if param_range is None:
        return True, None

    return validate_range(param_range.min, param_range.mean, param_range.max)


def validate_residue_data(residue_data: ResidueData) -> tuple[bool, List[str]]:
    """
    Validate complete ResidueData object.

    Args:
        residue_data: ResidueData object to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Validate required fields
    if not residue_data.name or residue_data.name.strip() == "":
        errors.append("Residue name is required")

    if not residue_data.category or residue_data.category.strip() == "":
        errors.append("Category is required")

    # Validate chemical parameters
    chem = residue_data.chemical_params

    if chem.bmp <= 0:
        errors.append(f"Invalid BMP value: {chem.bmp}")

    if chem.ts < 0 or chem.ts > 100:
        errors.append(f"Invalid TS value: {chem.ts} (must be 0-100%)")

    if chem.vs < 0 or chem.vs > 100:
        errors.append(f"Invalid VS value: {chem.vs} (must be 0-100%)")

    if chem.moisture < 0 or chem.moisture > 100:
        errors.append(f"Invalid moisture value: {chem.moisture} (must be 0-100%)")

    # Validate ranges
    if chem.bmp_range:
        valid, error = validate_parameter_range(chem.bmp_range)
        if not valid:
            errors.append(f"BMP range error: {error}")

    if chem.ts_range:
        valid, error = validate_parameter_range(chem.ts_range)
        if not valid:
            errors.append(f"TS range error: {error}")

    if chem.vs_range:
        valid, error = validate_parameter_range(chem.vs_range)
        if not valid:
            errors.append(f"VS range error: {error}")

    # Validate availability factors
    avail = residue_data.availability

    if avail.fc < 0 or avail.fc > 1:
        errors.append(f"Invalid FC (collection factor): {avail.fc} (must be 0-1)")

    if avail.fcp < 0 or avail.fcp > 1:
        errors.append(f"Invalid FCp (competition factor): {avail.fcp} (must be 0-1)")

    if avail.fs < 0 or avail.fs > 1:
        errors.append(f"Invalid FS (seasonal factor): {avail.fs} (must be 0-1)")

    if avail.fl < 0 or avail.fl > 1:
        errors.append(f"Invalid FL (logistic factor): {avail.fl} (must be 0-1)")

    if avail.final_availability < 0 or avail.final_availability > 100:
        errors.append(f"Invalid final availability: {avail.final_availability}% (must be 0-100%)")

    # Validate scenarios
    for scenario_name, ch4_value in residue_data.scenarios.items():
        if ch4_value < 0:
            errors.append(f"Invalid {scenario_name} scenario value: {ch4_value} (must be >= 0)")

    # Check scenario ordering (Pessimista <= Realista <= Otimista <= Teorico)
    scenarios = residue_data.scenarios
    if all(k in scenarios for k in ["Pessimista", "Realista", "Otimista", "Teórico (100%)"]):
        if scenarios["Pessimista"] > scenarios["Realista"]:
            errors.append("Pessimista scenario should be <= Realista scenario")
        if scenarios["Realista"] > scenarios["Otimista"]:
            errors.append("Realista scenario should be <= Otimista scenario")
        if scenarios["Otimista"] > scenarios["Teórico (100%)"]:
            errors.append("Otimista scenario should be <= Teorico scenario")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_lab_comparison(
    lab_value: float,
    lit_value: float,
    threshold_pct: float = 15.0
) -> Dict[str, Any]:
    """
    Validate laboratory value against literature reference.

    Args:
        lab_value: Laboratory measured value
        lit_value: Literature reference value
        threshold_pct: Acceptable deviation threshold (%)

    Returns:
        Dictionary with validation results
    """
    if lit_value == 0:
        return {
            "status": "error",
            "deviation_pct": 0,
            "message": "Literature value is zero, cannot compare"
        }

    deviation_pct = ((lab_value - lit_value) / lit_value) * 100
    abs_deviation = abs(deviation_pct)

    if abs_deviation <= threshold_pct:
        status = "within_range"
        icon = "[OK]"
        message = f"Dentro da faixa aceitavel (+/-{threshold_pct}%)"
    elif abs_deviation <= threshold_pct * 1.5:
        status = "acceptable"
        icon = "[WARN]"
        message = f"Desvio aceitavel (ate {threshold_pct * 1.5}%)"
    else:
        status = "out_of_range"
        icon = "[ERROR]"
        message = f"Fora da faixa aceitavel (>{threshold_pct * 1.5}%)"

    return {
        "status": status,
        "icon": icon,
        "deviation_pct": deviation_pct,
        "abs_deviation": abs_deviation,
        "threshold": threshold_pct,
        "message": message,
        "lab_value": lab_value,
        "lit_value": lit_value
    }


def check_data_completeness(residue_data: ResidueData) -> Dict[str, Any]:
    """
    Check completeness of residue data.

    Args:
        residue_data: ResidueData object

    Returns:
        Dictionary with completeness metrics
    """
    total_fields = 0
    filled_fields = 0
    missing_fields = []

    # Check chemical parameters
    chem = residue_data.chemical_params
    chem_fields = [
        ('BMP', chem.bmp),
        ('TS', chem.ts),
        ('VS', chem.vs),
        ('Moisture', chem.moisture),
        ('C:N Ratio', chem.cn_ratio),
        ('pH', chem.ph),
        ('COD', chem.cod),
        ('CH4 Content', chem.ch4_content)
    ]

    for field_name, value in chem_fields:
        total_fields += 1
        if value is not None and value > 0:
            filled_fields += 1
        else:
            missing_fields.append(f"Chemical: {field_name}")

    # Check ranges
    range_fields = [
        ('BMP Range', chem.bmp_range),
        ('TS Range', chem.ts_range),
        ('VS Range', chem.vs_range),
        ('CN Ratio Range', chem.cn_ratio_range)
    ]

    for field_name, range_obj in range_fields:
        total_fields += 1
        if range_obj and range_obj.has_range():
            filled_fields += 1
        else:
            missing_fields.append(f"Range: {field_name}")

    # Check references
    total_fields += 1
    if residue_data.references and len(residue_data.references) > 0:
        filled_fields += 1
    else:
        missing_fields.append("Scientific References")

    completeness_pct = (filled_fields / total_fields * 100) if total_fields > 0 else 0

    return {
        "completeness_pct": completeness_pct,
        "total_fields": total_fields,
        "filled_fields": filled_fields,
        "missing_fields": missing_fields,
        "is_complete": completeness_pct >= 80  # Consider 80%+ as complete
    }


__all__ = [
    'validate_range',
    'validate_parameter_range',
    'validate_residue_data',
    'validate_lab_comparison',
    'check_data_completeness'
]
