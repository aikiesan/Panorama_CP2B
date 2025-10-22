"""
Residue Data Models - Clean Data Structures (SOLID: Single Responsibility)
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

This module contains only dataclass definitions - no data, no business logic.
Follows the Single Responsibility Principle: defines structure only.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class ParameterRange:
    """Represents a parameter with min, mean, and max values"""
    min: Optional[float] = None
    mean: Optional[float] = None
    max: Optional[float] = None
    unit: Optional[str] = None

    def __post_init__(self):
        """Validate that at least mean is provided"""
        if self.mean is None and self.min is None and self.max is None:
            raise ValueError("At least one value (min, mean, or max) must be provided")

    def to_display(self) -> str:
        """Format range for display"""
        unit_str = f" {self.unit}" if self.unit else ""

        if self.min is not None and self.max is not None and self.mean is not None:
            return f"{self.min:.1f} - {self.mean:.1f} - {self.max:.1f}{unit_str}"
        elif self.min is not None and self.max is not None:
            return f"{self.min:.1f} - {self.max:.1f}{unit_str}"
        elif self.mean is not None:
            return f"{self.mean:.1f}{unit_str}"
        else:
            return "N/A"

    def has_range(self) -> bool:
        """Check if this parameter has range data (min/max)"""
        return self.min is not None or self.max is not None


@dataclass
class ChemicalParameters:
    """Chemical composition and methane potential parameters"""
    bmp: float
    bmp_unit: str
    ts: float
    vs: float
    vs_basis: str
    moisture: float
    cn_ratio: Optional[float] = None
    ph: Optional[float] = None
    cod: Optional[float] = None
    nitrogen: Optional[float] = None
    carbon: Optional[float] = None
    ch4_content: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    protein: Optional[float] = None
    toc: Optional[float] = None

    # Range data from literature validation
    bmp_range: Optional[ParameterRange] = None
    ts_range: Optional[ParameterRange] = None
    vs_range: Optional[ParameterRange] = None
    moisture_range: Optional[ParameterRange] = None
    cn_ratio_range: Optional[ParameterRange] = None
    ph_range: Optional[ParameterRange] = None
    cod_range: Optional[ParameterRange] = None
    nitrogen_range: Optional[ParameterRange] = None
    carbon_range: Optional[ParameterRange] = None
    ch4_content_range: Optional[ParameterRange] = None
    phosphorus_range: Optional[ParameterRange] = None
    potassium_range: Optional[ParameterRange] = None
    protein_range: Optional[ParameterRange] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for display"""
        result = {
            "BMP": f"{self.bmp} {self.bmp_unit}",
            "Sólidos Totais (TS)": f"{self.ts}%",
            "Sólidos Voláteis (VS)": f"{self.vs}% {self.vs_basis}",
            "Umidade": f"{self.moisture}%"
        }
        if self.cn_ratio: result["Relação C:N"] = f"{self.cn_ratio}"
        if self.ph: result["pH"] = f"{self.ph}"
        if self.cod: result["DQO"] = f"{self.cod} mg/L"
        if self.nitrogen: result["Nitrogênio (N)"] = f"{self.nitrogen}%"
        if self.carbon: result["Carbono (C)"] = f"{self.carbon}%"
        if self.ch4_content: result["Conteúdo CH₄"] = f"{self.ch4_content}%"
        return result

    def to_range_table(self) -> List[Dict[str, str]]:
        """
        Convert chemical parameters to table format showing MIN/MEAN/MAX ranges
        Returns list of dicts for DataFrame display
        """
        ranges_data = []

        param_mapping = [
            ("BMP", self.bmp, self.bmp_range, self.bmp_unit),
            ("Sólidos Totais (ST)", self.ts, self.ts_range, "%"),
            ("Sólidos Voláteis (SV)", self.vs, self.vs_range, "% ST"),
            ("Umidade", self.moisture, self.moisture_range, "%"),
            ("Relação C:N", self.cn_ratio, self.cn_ratio_range, ""),
            ("pH", self.ph, self.ph_range, ""),
            ("DQO", self.cod, self.cod_range, "mg/L"),
            ("Nitrogênio (N)", self.nitrogen, self.nitrogen_range, "%"),
            ("Carbono (C)", self.carbon, self.carbon_range, "%"),
            ("Conteúdo CH₄", self.ch4_content, self.ch4_content_range, "%"),
            ("Fósforo (P₂O₅)", self.phosphorus, self.phosphorus_range, "%"),
            ("Potássio (K₂O)", self.potassium, self.potassium_range, "%"),
            ("Proteína", self.protein, self.protein_range, "%"),
        ]

        for param_name, value, range_obj, unit in param_mapping:
            if value is None:
                continue

            if range_obj and range_obj.has_range():
                ranges_data.append({
                    "Parâmetro": param_name,
                    "Mínimo": f"{range_obj.min:.2f}" if range_obj.min is not None else "-",
                    "Média/Valor": f"{value:.2f}",
                    "Máximo": f"{range_obj.max:.2f}" if range_obj.max is not None else "-",
                    "Unidade": unit
                })
            else:
                # No range data, show only mean value
                ranges_data.append({
                    "Parâmetro": param_name,
                    "Mínimo": "-",
                    "Média/Valor": f"{value:.2f}",
                    "Máximo": "-",
                    "Unidade": unit
                })

        return ranges_data


@dataclass
class AvailabilityFactors:
    """Availability correction factors for residues"""
    fc: float
    fcp: float
    fs: float
    fl: float
    final_availability: float

    # Range data from literature validation
    fc_range: Optional[ParameterRange] = None
    fcp_range: Optional[ParameterRange] = None
    fs_range: Optional[ParameterRange] = None
    fl_range: Optional[ParameterRange] = None

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for display"""
        return {
            "FC (Coleta)": f"{self.fc:.2f}",
            "FCp (Competição)": f"{self.fcp:.2f}",
            "FS (Sazonal)": f"{self.fs:.2f}",
            "FL (Logístico)": f"{self.fl:.2f}",
            "Disponibilidade Final": f"{self.final_availability:.1f}%"
        }

    def to_range_table(self) -> List[Dict[str, str]]:
        """
        Convert availability factors to table format showing MIN/MEAN/MAX ranges
        Returns list of dicts for DataFrame display
        """
        ranges_data = []

        param_mapping = [
            ("FC (Fator de Coleta)", self.fc, self.fc_range, "Eficiência de recolhimento"),
            ("FCp (Fator de Competição)", self.fcp, self.fcp_range, "Competição por usos alternativos"),
            ("FS (Fator Sazonal)", self.fs, self.fs_range, "Variação sazonal"),
            ("FL (Fator Logístico)", self.fl, self.fl_range, "Restrição por distância"),
        ]

        for param_name, value, range_obj, justification in param_mapping:
            if range_obj and range_obj.has_range():
                ranges_data.append({
                    "Fator": param_name,
                    "Mínimo": f"{range_obj.min:.2f}" if range_obj.min is not None else "-",
                    "Valor Adotado": f"{value:.2f}",
                    "Máximo": f"{range_obj.max:.2f}" if range_obj.max is not None else "-",
                    "Justificativa": justification
                })
            else:
                ranges_data.append({
                    "Fator": param_name,
                    "Mínimo": "-",
                    "Valor Adotado": f"{value:.2f}",
                    "Máximo": "-",
                    "Justificativa": justification
                })

        # Add final availability row
        ranges_data.append({
            "Fator": "Disponibilidade Final (FDE)",
            "Mínimo": "-",
            "Valor Adotado": f"{self.final_availability:.1f}%",
            "Máximo": "-",
            "Justificativa": "Produto de todos os fatores"
        })

        return ranges_data


@dataclass
class OperationalParameters:
    """Operational parameters for anaerobic digestion"""
    hrt: str
    temperature: str
    fi_ratio: Optional[float] = None
    olr: Optional[str] = None
    reactor_type: Optional[str] = None
    tan_threshold: Optional[str] = None
    vfa_limit: Optional[str] = None

    # Range data from literature validation (TRH in days, Temperature in °C)
    hrt_range: Optional[ParameterRange] = None
    temperature_range: Optional[ParameterRange] = None

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for display"""
        result = {
            "TRH (Tempo de Retenção Hidráulica)": self.hrt,
            "Temperatura": self.temperature,
        }
        if self.fi_ratio: result["Razão F/I"] = f"{self.fi_ratio}"
        if self.olr: result["TCO (Taxa de Carga Orgânica)"] = self.olr
        if self.reactor_type: result["Tipo de Reator"] = self.reactor_type
        if self.tan_threshold: result["Limite TAN"] = self.tan_threshold
        if self.vfa_limit: result["Limite AGV"] = self.vfa_limit
        return result

    def to_range_table(self) -> List[Dict[str, str]]:
        """
        Convert operational parameters to table format showing MIN/MEAN/MAX ranges
        Returns list of dicts for DataFrame display
        """
        ranges_data = []

        # TRH and Temperature with ranges
        if self.hrt_range and self.hrt_range.has_range():
            ranges_data.append({
                "Parâmetro": "TRH (Tempo de Retenção Hidráulica)",
                "Mínimo": f"{self.hrt_range.min:.0f} dias" if self.hrt_range.min else "-",
                "Valor Operacional": self.hrt,
                "Máximo": f"{self.hrt_range.max:.0f} dias" if self.hrt_range.max else "-",
            })
        else:
            ranges_data.append({
                "Parâmetro": "TRH (Tempo de Retenção Hidráulica)",
                "Mínimo": "-",
                "Valor Operacional": self.hrt,
                "Máximo": "-",
            })

        if self.temperature_range and self.temperature_range.has_range():
            ranges_data.append({
                "Parâmetro": "Temperatura",
                "Mínimo": f"{self.temperature_range.min:.0f}°C" if self.temperature_range.min else "-",
                "Valor Operacional": self.temperature,
                "Máximo": f"{self.temperature_range.max:.0f}°C" if self.temperature_range.max else "-",
            })
        else:
            ranges_data.append({
                "Parâmetro": "Temperatura",
                "Mínimo": "-",
                "Valor Operacional": self.temperature,
                "Máximo": "-",
            })

        # Other parameters (no ranges)
        if self.fi_ratio:
            ranges_data.append({
                "Parâmetro": "Razão F/I (Alimento/Inóculo)",
                "Mínimo": "-",
                "Valor Operacional": f"{self.fi_ratio}",
                "Máximo": "-",
            })

        if self.olr:
            ranges_data.append({
                "Parâmetro": "TCO (Taxa de Carga Orgânica)",
                "Mínimo": "-",
                "Valor Operacional": self.olr,
                "Máximo": "-",
            })

        if self.reactor_type:
            ranges_data.append({
                "Parâmetro": "Tipo de Reator",
                "Mínimo": "-",
                "Valor Operacional": self.reactor_type,
                "Máximo": "-",
            })

        return ranges_data


@dataclass
class ScientificReference:
    """Scientific paper reference"""
    title: str
    authors: str
    year: int
    doi: Optional[str] = None
    scopus_link: Optional[str] = None
    journal: Optional[str] = None
    relevance: str = "High"
    key_findings: List[str] = None
    data_type: str = "Literatura Científica"

    def __post_init__(self):
        if self.key_findings is None:
            self.key_findings = []


@dataclass
class ResidueData:
    """Complete residue data with validated factors"""
    name: str
    category: str
    icon: str
    generation: str
    destination: str
    chemical_params: ChemicalParameters
    availability: AvailabilityFactors
    operational: OperationalParameters
    justification: str
    scenarios: Dict[str, float]
    references: List[ScientificReference]
    top_municipalities: Optional[List[Dict]] = None
    validation_data: Optional[Dict] = None
    contribution_breakdown: Optional[Dict] = None
    sub_residues: Optional[List['ResidueData']] = None

    # Unified database metadata fields
    source_origin: str = "PanoramaCP2B"  # Data origin: "PanoramaCP2B" or "Jupyter"
    municipal_data: Optional[Dict[str, float]] = None  # {municipality: potential} aggregation
    validation_source: Optional[str] = None  # "Google Earth Engine", "MapBiomas", etc
    total_plants: Optional[int] = None  # Number of plants for this culture
    municipalities_count: Optional[int] = None  # Number of municipalities
    state_rank: Optional[int] = None  # State rank by potential

    # Phase 5: FDE Validation Fields (from cp2b_analise_fatores_residuos.md)
    fde_real: Optional[float] = None  # Real Fator de Disponibilidade Efetiva (percentage, e.g., 80.75)
    priority_tier: Optional[str] = None  # Priority tier: "EXCEPCIONAL", "EXCELENTE", "BOM", "REGULAR", "BAIXO", "CRÍTICO", "INVIÁVEL"
    recommendation: Optional[str] = None  # Strategic recommendation from Phase 5 analysis
    fde_rank: Optional[int] = None  # Rank position in FDE ranking (1 = highest)

    # Individual FDE factors for transparency
    fc_value: Optional[float] = None  # Fator de Coleta (0.55-0.95)
    fcp_value: Optional[float] = None  # Fator de Competição (can be >1)
    fs_value: Optional[float] = None  # Fator Sazonalidade (0.70-1.0)
    fl_value: Optional[float] = None  # Fator Logístico (0.65-1.0)

    # Hierarchical structure fields (for parent-child organization by culture)
    culture_group: Optional[str] = None  # Parent culture (e.g., "Cana-de-Açúcar", "Café", "Citros")
    parent_residue: Optional[str] = None  # Name of parent residue if this is a sub-residue
    is_composite: bool = False  # True if this is a composite/parent residue

    # Backward compatibility properties for SAF -> FDE transition
    @property
    def saf_real(self) -> Optional[float]:
        """Backward compatibility: saf_real -> fde_real"""
        return self.fde_real

    @saf_real.setter
    def saf_real(self, value: Optional[float]):
        """Backward compatibility: saf_real -> fde_real"""
        self.fde_real = value

    @property
    def saf_rank(self) -> Optional[int]:
        """Backward compatibility: saf_rank -> fde_rank"""
        return self.fde_rank

    @saf_rank.setter
    def saf_rank(self, value: Optional[int]):
        """Backward compatibility: saf_rank -> fde_rank"""
        self.fde_rank = value

    def __post_init__(self):
        """Validate residue data on initialization"""
        from src.utils.validators import validate_residue_data

        is_valid, errors = validate_residue_data(self)
        if not is_valid:
            print(f"[WARNING] Validation issues in {self.name}:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"  - {error}")

    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate complete residue data.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        from src.utils.validators import validate_residue_data
        return validate_residue_data(self)

    def check_completeness(self) -> Dict[str, Any]:
        """
        Check data completeness.

        Returns:
            Dictionary with completeness metrics
        """
        from src.utils.validators import check_data_completeness
        return check_data_completeness(self)

    def to_summary_dict(self) -> Dict[str, Any]:
        """
        Convert to summary dictionary for display.

        Returns:
            Dictionary with key residue information
        """
        return {
            "name": self.name,
            "category": self.category,
            "icon": self.icon,
            "bmp": self.chemical_params.bmp,
            "bmp_unit": self.chemical_params.bmp_unit,
            "availability": self.availability.final_availability,
            "realistic_potential": self.scenarios.get("Realista", 0),
            "references_count": len(self.references)
        }

    def get_sub_residue(self, name: str) -> Optional['ResidueData']:
        """
        Get a sub-residue by name.

        Useful for accessing specific sub-components of composite residues.
        For example, getting "Palha" from Cana-de-açúcar.

        Args:
            name: Name of the sub-residue to find

        Returns:
            ResidueData object if found, None otherwise

        Example:
            >>> palha = cana_data.get_sub_residue("Palha de Cana-de-açúcar (Palhiço)")
            >>> if palha:
            ...     print(f"Found: {palha.name}")
        """
        if not self.sub_residues:
            return None

        for sub_residue in self.sub_residues:
            if sub_residue.name == name:
                return sub_residue

        return None

    def get_total_ch4(self, scenario: str = 'Realista') -> float:
        """
        Calculate total CH4 potential from all sub-residues.

        If the residue has sub-residues, returns their sum.
        If no sub-residues, returns the residue's own scenario value.

        Args:
            scenario: Which scenario to sum ('Pessimista', 'Realista', 'Otimista', 'Teórico')

        Returns:
            Total CH4 potential for the scenario

        Example:
            >>> total = cana_data.get_total_ch4('Realista')
            >>> total
            6077.0  # Sum of Bagaço + Palha + Vinhaça + Torta
        """
        if not self.sub_residues:
            # No sub-residues, return own value
            return self.scenarios.get(scenario, 0.0)

        # Sum sub-residues
        total = 0.0
        for sub_residue in self.sub_residues:
            sub_ch4 = sub_residue.scenarios.get(scenario, 0.0)
            total += sub_ch4

        return total

    def has_sub_residues(self) -> bool:
        """
        Check if this residue has sub-residues.

        Useful for conditional logic in UI components.

        Returns:
            True if sub_residues list exists and is not empty

        Example:
            >>> if cana_data.has_sub_residues():
            ...     print("This is a composite residue")
        """
        return self.sub_residues is not None and len(self.sub_residues) > 0

    def get_sub_residue_count(self) -> int:
        """
        Get the count of sub-residues.

        Returns:
            Number of sub-residues, 0 if none

        Example:
            >>> count = cana_data.get_sub_residue_count()
            >>> count
            4  # Bagaço, Palha, Vinhaça, Torta
        """
        if not self.sub_residues:
            return 0
        return len(self.sub_residues)
