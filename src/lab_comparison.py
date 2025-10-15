"""
Laboratory Data Comparison Module
CP2B - Tool for comparing empirical lab results with validated literature references
"""

import streamlit as st
import pandas as pd
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

from src.models.residue_models import ChemicalParameters, ResidueData


@dataclass
class LabResult:
    """Laboratory measurement result"""
    parameter: str
    measured_value: float
    unit: str
    measurement_date: Optional[str] = None
    lab_name: Optional[str] = None
    notes: Optional[str] = None


class LabComparison:
    """
    Handles comparison between laboratory results and literature references
    """

    # Acceptable deviation thresholds (%)
    THRESHOLDS = {
        'bmp': 15.0,  # ±15% for BMP
        'ts': 10.0,   # ±10% for Total Solids
        'vs': 10.0,   # ±10% for Volatile Solids
        'moisture': 10.0,  # ±10% for moisture
        'cn_ratio': 20.0,  # ±20% for C:N ratio (more variable)
        'ph': 5.0,   # ±5% for pH
        'cod': 20.0,  # ±20% for COD
        'nitrogen': 15.0,  # ±15% for nitrogen
        'carbon': 15.0,   # ±15% for carbon
        'ch4_content': 10.0  # ±10% for CH₄ content
    }

    def __init__(self, residue_data: ResidueData):
        """Initialize with residue reference data"""
        self.residue_data = residue_data
        self.chemical_params = residue_data.chemical_params

    def calculate_deviation(self, measured: float, reference: float) -> float:
        """Calculate percentage deviation from reference"""
        if reference == 0:
            return 0.0
        return ((measured - reference) / reference) * 100

    def get_validation_status(self, parameter: str, deviation: float) -> Tuple[str, str]:
        """
        Get validation status based on deviation

        Returns:
            Tuple of (status_emoji, status_text)
        """
        threshold = self.THRESHOLDS.get(parameter, 15.0)
        abs_deviation = abs(deviation)

        if abs_deviation <= threshold:
            return ("✅", "Dentro da faixa")
        elif abs_deviation <= threshold * 1.5:
            return ("⚠️", "Desvio aceitável")
        else:
            return ("❌", "Fora da faixa")

    def compare_parameter(self, parameter: str, measured_value: float) -> Dict:
        """
        Compare a single parameter with reference

        Args:
            parameter: Parameter name (e.g., 'bmp', 'ts', 'vs')
            measured_value: Measured laboratory value

        Returns:
            Dictionary with comparison results
        """
        # Get reference value
        reference_value = None
        parameter_name = ""
        unit = ""

        if parameter == 'bmp':
            reference_value = self.chemical_params.bmp
            parameter_name = "BMP (Potencial Metanogênico)"
            unit = self.chemical_params.bmp_unit
        elif parameter == 'ts':
            reference_value = self.chemical_params.ts
            parameter_name = "Sólidos Totais (TS)"
            unit = "%"
        elif parameter == 'vs':
            reference_value = self.chemical_params.vs
            parameter_name = "Sólidos Voláteis (VS)"
            unit = f"% {self.chemical_params.vs_basis}"
        elif parameter == 'moisture':
            reference_value = self.chemical_params.moisture
            parameter_name = "Umidade"
            unit = "%"
        elif parameter == 'cn_ratio' and self.chemical_params.cn_ratio:
            reference_value = self.chemical_params.cn_ratio
            parameter_name = "Relação C:N"
            unit = ""
        elif parameter == 'ph' and self.chemical_params.ph:
            reference_value = self.chemical_params.ph
            parameter_name = "pH"
            unit = ""
        elif parameter == 'nitrogen' and self.chemical_params.nitrogen:
            reference_value = self.chemical_params.nitrogen
            parameter_name = "Nitrogênio (N)"
            unit = "%"
        elif parameter == 'carbon' and self.chemical_params.carbon:
            reference_value = self.chemical_params.carbon
            parameter_name = "Carbono (C)"
            unit = "%"
        elif parameter == 'ch4_content' and self.chemical_params.ch4_content:
            reference_value = self.chemical_params.ch4_content
            parameter_name = "Conteúdo CH₄"
            unit = "%"
        else:
            return None

        if reference_value is None:
            return None

        # Calculate deviation
        deviation = self.calculate_deviation(measured_value, reference_value)
        status_emoji, status_text = self.get_validation_status(parameter, deviation)

        return {
            'parameter': parameter_name,
            'reference': reference_value,
            'measured': measured_value,
            'unit': unit,
            'deviation': deviation,
            'status_emoji': status_emoji,
            'status_text': status_text
        }

    def create_comparison_report(self, lab_results: Dict[str, float]) -> pd.DataFrame:
        """
        Create a complete comparison report

        Args:
            lab_results: Dictionary of parameter_name -> measured_value

        Returns:
            DataFrame with comparison results
        """
        comparisons = []

        for param, measured_value in lab_results.items():
            comparison = self.compare_parameter(param, measured_value)
            if comparison:
                comparisons.append({
                    'Parâmetro': comparison['parameter'],
                    'Referência Literatura': f"{comparison['reference']:.2f} {comparison['unit']}",
                    'Valor Medido (Lab)': f"{comparison['measured']:.2f} {comparison['unit']}",
                    'Desvio (%)': f"{comparison['deviation']:+.1f}%",
                    'Status': f"{comparison['status_emoji']} {comparison['status_text']}"
                })

        return pd.DataFrame(comparisons)


# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

def initialize_lab_session():
    """Initialize session state for lab data storage"""
    if 'lab_results' not in st.session_state:
        st.session_state.lab_results = {}
    if 'lab_metadata' not in st.session_state:
        st.session_state.lab_metadata = {
            'lab_name': '',
            'measurement_date': None,
            'operator': '',
            'notes': ''
        }


def save_lab_result(residue_name: str, parameter: str, value: float):
    """Save a lab result to session state"""
    if residue_name not in st.session_state.lab_results:
        st.session_state.lab_results[residue_name] = {}
    st.session_state.lab_results[residue_name][parameter] = value


def get_lab_results(residue_name: str) -> Optional[Dict[str, float]]:
    """Get all lab results for a specific residue"""
    return st.session_state.lab_results.get(residue_name)


def clear_lab_results(residue_name: str):
    """Clear all lab results for a specific residue"""
    if residue_name in st.session_state.lab_results:
        del st.session_state.lab_results[residue_name]


def export_comparison_report(comparison_df: pd.DataFrame, residue_name: str) -> bytes:
    """
    Export comparison report as CSV

    Args:
        comparison_df: DataFrame with comparison results
        residue_name: Name of the residue

    Returns:
        CSV data as bytes
    """
    return comparison_df.to_csv(index=False).encode('utf-8-sig')
