"""
Scenario Manager Service
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Manage availability scenarios with different factor combinations.
Implements 4 scenario types: Pessimista, Realista, Otimista, Teórico (100%)

SOLID Compliance:
- Single Responsibility: Only manages scenario factor adjustments
- Open/Closed: Easy to add new scenarios without modifying calculator
- Liskov Substitution: Compatible interface with AvailabilityCalculator
- Interface Segregation: Focused, minimal public methods
- Dependency Inversion: Depends on data model abstractions, not UI
"""

from typing import Dict, Optional
from src.models.residue_models import ResidueData
from src.services.availability_calculator import AvailabilityCalculator


class ScenarioManager:
    """
    Manage availability scenarios with different factor combinations.

    Maps 4 scenarios to factor adjustments using ParameterRange min/mean/max:
    - Pessimista: Uses min values (conservative, max competition)
    - Realista: Uses mean values (calibrated real-world baseline)
    - Otimista: Uses max values (optimistic, min competition)
    - Teórico (100%): Theoretical maximum (no competition constraints)

    Example:
        >>> residue_data = get_residue_data("Palha de Cana")
        >>> manager = ScenarioManager()
        >>> factors = manager.get_scenario_factors("Realista", residue_data)
        >>> comparison = manager.compare_scenarios(residue_data)
    """

    SCENARIOS = {
        'Pessimista': 'Conservative factors (max competition)',
        'Realista': 'Calibrated real-world factors (baseline)',
        'Otimista': 'Optimistic factors (min competition)',
        'Teórico (100%)': 'No competition (theoretical max)',
    }

    @staticmethod
    def get_scenario_factors(
        scenario_name: str,
        residue_data: ResidueData
    ) -> Dict[str, float]:
        """
        Get adjusted factors for a specific scenario.

        Maps scenarios to ParameterRange values:
        - Pessimista → min
        - Realista → mean
        - Otimista → max
        - Teórico → 1.0 (no constraints)

        Args:
            scenario_name: One of 'Pessimista', 'Realista', 'Otimista', 'Teórico (100%)'
            residue_data: ResidueData object with availability factors and ranges

        Returns:
            Dictionary with adjusted factors:
                {
                    'fc': float,
                    'fcp': float,
                    'fs': float,
                    'fl': float,
                    'scenario': str
                }

        Raises:
            ValueError: If scenario_name is invalid
            AttributeError: If residue_data lacks required ranges

        Example:
            >>> factors = ScenarioManager.get_scenario_factors(
            ...     "Realista",
            ...     palha_cana_data
            ... )
            >>> factors
            {'fc': 0.80, 'fcp': 0.65, 'fs': 1.0, 'fl': 0.90, 'scenario': 'Realista'}
        """
        if scenario_name not in ScenarioManager.SCENARIOS:
            raise ValueError(
                f"Invalid scenario '{scenario_name}'. "
                f"Must be one of: {', '.join(ScenarioManager.SCENARIOS.keys())}"
            )

        availability = residue_data.availability

        if scenario_name == 'Pessimista':
            # Conservative: use min values for positive factors
            # For FCp (competition), use max (higher competition = less available)
            return {
                'fc': availability.fc_range.min if availability.fc_range and availability.fc_range.min else availability.fc,
                'fcp': availability.fcp_range.max if availability.fcp_range and availability.fcp_range.max else availability.fcp,
                'fs': availability.fs_range.min if availability.fs_range and availability.fs_range.min else availability.fs,
                'fl': availability.fl_range.min if availability.fl_range and availability.fl_range.min else availability.fl,
                'scenario': 'Pessimista'
            }

        elif scenario_name == 'Realista':
            # Baseline: use mean values
            return {
                'fc': availability.fc_range.mean if availability.fc_range and availability.fc_range.mean else availability.fc,
                'fcp': availability.fcp_range.mean if availability.fcp_range and availability.fcp_range.mean else availability.fcp,
                'fs': availability.fs_range.mean if availability.fs_range and availability.fs_range.mean else availability.fs,
                'fl': availability.fl_range.mean if availability.fl_range and availability.fl_range.mean else availability.fl,
                'scenario': 'Realista'
            }

        elif scenario_name == 'Otimista':
            # Optimistic: use max for positive factors, min for competition
            return {
                'fc': availability.fc_range.max if availability.fc_range and availability.fc_range.max else availability.fc,
                'fcp': availability.fcp_range.min if availability.fcp_range and availability.fcp_range.min else availability.fcp,
                'fs': availability.fs_range.max if availability.fs_range and availability.fs_range.max else availability.fs,
                'fl': availability.fl_range.max if availability.fl_range and availability.fl_range.max else availability.fl,
                'scenario': 'Otimista'
            }

        else:  # Teórico (100%)
            # Theoretical max: no competition, maximum efficiency
            return {
                'fc': 1.0,  # Perfect collection
                'fcp': 0.0,  # No competition
                'fs': 1.0,  # Year-round availability
                'fl': 1.0,  # Perfect logistics
                'scenario': 'Teórico (100%)'
            }

    @staticmethod
    def compare_scenarios(
        residue_data: ResidueData
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare all 4 scenarios for a residue with calculated potentials.

        For each scenario, applies adjusted factors to AvailabilityCalculator
        and calculates resulting CH4 potential.

        Args:
            residue_data: ResidueData object with complete data

        Returns:
            Dictionary with structure:
                {
                    'Pessimista': {
                        'availability': 10.2,
                        'ch4': 1250.5,
                        'factors': {'fc': ..., 'fcp': ..., 'fs': ..., 'fl': ...}
                    },
                    'Realista': {...},
                    'Otimista': {...},
                    'Teórico (100%)': {...}
                }

        Example:
            >>> comparison = ScenarioManager.compare_scenarios(cana_data)
            >>> comparison['Realista']['availability']
            25.2
            >>> comparison['Teórico (100%)']['availability']
            100.0
        """
        results = {}

        for scenario_name in ScenarioManager.SCENARIOS.keys():
            # Get adjusted factors for this scenario
            factors = ScenarioManager.get_scenario_factors(scenario_name, residue_data)

            # Calculate availability percentage using adjusted factors
            availability_pct = AvailabilityCalculator.calculate(
                fc=factors['fc'],
                fcp=factors['fcp'],
                fs=factors['fs'],
                fl=factors['fl']
            )

            # Get CH4 potential from scenarios dict
            ch4_potential = residue_data.scenarios.get(scenario_name, 0.0)

            results[scenario_name] = {
                'availability': availability_pct,
                'ch4': ch4_potential,
                'factors': {
                    'fc': factors['fc'],
                    'fcp': factors['fcp'],
                    'fs': factors['fs'],
                    'fl': factors['fl']
                }
            }

        return results

    @staticmethod
    def calculate_reduction(
        realistic: float,
        theoretical: float
    ) -> float:
        """
        Calculate percentage reduction from theoretical to realistic scenario.

        Shows how much real-world constraints reduce the theoretical maximum.

        Args:
            realistic: Realistic scenario value (typically from scenarios dict)
            theoretical: Theoretical scenario value (100% availability)

        Returns:
            Reduction percentage (0-100)
            Returns 0 if theoretical is 0

        Example:
            >>> reduction = ScenarioManager.calculate_reduction(25.2, 100.0)
            >>> reduction
            74.8  # 74.8% reduction from theoretical
        """
        if theoretical <= 0:
            return 0.0

        reduction = ((theoretical - realistic) / theoretical * 100)
        return round(reduction, 2)

    @staticmethod
    def get_scenario_description(scenario_name: str) -> str:
        """
        Get human-readable description of a scenario.

        Args:
            scenario_name: One of the valid scenario names

        Returns:
            Description string

        Example:
            >>> desc = ScenarioManager.get_scenario_description("Otimista")
            >>> desc
            'Optimistic factors (min competition)'
        """
        return ScenarioManager.SCENARIOS.get(
            scenario_name,
            "Unknown scenario"
        )

    @staticmethod
    def validate_scenario(scenario_name: str) -> tuple[bool, str]:
        """
        Validate if scenario name is valid.

        Args:
            scenario_name: Scenario name to validate

        Returns:
            Tuple of (is_valid, message)

        Example:
            >>> is_valid, msg = ScenarioManager.validate_scenario("Realista")
            >>> is_valid
            True
        """
        if scenario_name in ScenarioManager.SCENARIOS:
            return True, f"Valid scenario: {scenario_name}"
        else:
            valid_names = ", ".join(ScenarioManager.SCENARIOS.keys())
            return False, f"Invalid scenario. Valid options: {valid_names}"
