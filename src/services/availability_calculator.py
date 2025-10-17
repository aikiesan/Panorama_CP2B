"""
Availability Calculator Service
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Calculate final availability using validated methodology
Implements the formula: D_final = FC × (1 - FCp) × FS × FL × 100%

Based on validated research methodology from 15+ scientific papers.
"""

from typing import Dict, Optional


class AvailabilityCalculator:
    """
    Pure calculation logic for residue availability.

    Methodology:
    - FC (Collection Factor): Technical collection efficiency (0-1)
    - FCp (Competition Factor): Fraction competed by alternative uses (0-1)
    - FS (Seasonal Factor): Seasonal availability variation (0-1)
    - FL (Logistic Factor): Restriction by economic distance (0-1)

    Formula: D_final = FC × (1 - FCp) × FS × FL × 100%

    Example:
        >>> calc = AvailabilityCalculator()
        >>> calc.calculate(fc=0.80, fcp=0.65, fs=1.0, fl=0.90)
        25.2  # Palha de cana availability
    """

    @staticmethod
    def calculate(
        fc: float,
        fcp: float,
        fs: float,
        fl: float
    ) -> float:
        """
        Calculate final availability percentage.

        Args:
            fc: Collection factor (0-1)
            fcp: Competition factor (0-1)
            fs: Seasonal factor (0-1)
            fl: Logistic factor (0-1)

        Returns:
            Final availability as percentage (0-100)

        Raises:
            ValueError: If any factor is outside [0, 1] range

        Example:
            >>> AvailabilityCalculator.calculate(0.80, 0.65, 1.0, 0.90)
            25.2
        """
        # Validate inputs
        factors = {'FC': fc, 'FCp': fcp, 'FS': fs, 'FL': fl}
        for name, value in factors.items():
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must be between 0 and 1, got {value}")

        # Apply formula
        availability = fc * (1 - fcp) * fs * fl * 100

        return round(availability, 2)

    @staticmethod
    def calculate_from_factors(
        fc: float,
        fcp: float,
        fs: float,
        fl: float,
        generation_total: float,
        unit: str = "ton"
    ) -> Dict[str, float]:
        """
        Calculate both percentage and absolute available amount.

        Args:
            fc: Collection factor
            fcp: Competition factor
            fs: Seasonal factor
            fl: Logistic factor
            generation_total: Total generation amount
            unit: Unit of measurement (ton, m³, etc.)

        Returns:
            Dictionary with:
                - 'percentage': Availability percentage
                - 'available_amount': Absolute available amount
                - 'total_generation': Total generation
                - 'unit': Unit of measurement

        Example:
            >>> calc = AvailabilityCalculator()
            >>> result = calc.calculate_from_factors(
            ...     fc=0.80, fcp=0.65, fs=1.0, fl=0.90,
            ...     generation_total=122_900_000, unit="ton"
            ... )
            >>> result['percentage']
            25.2
            >>> result['available_amount']
            30970800.0
        """
        percentage = AvailabilityCalculator.calculate(fc, fcp, fs, fl)
        available_amount = generation_total * (percentage / 100)

        return {
            'percentage': percentage,
            'available_amount': available_amount,
            'total_generation': generation_total,
            'unit': unit
        }

    @staticmethod
    def explain_calculation(
        fc: float,
        fcp: float,
        fs: float,
        fl: float
    ) -> str:
        """
        Generate step-by-step explanation of calculation.

        Args:
            fc: Collection factor
            fcp: Competition factor
            fs: Seasonal factor
            fl: Logistic factor

        Returns:
            Formatted string explaining the calculation

        Example:
            >>> calc = AvailabilityCalculator()
            >>> print(calc.explain_calculation(0.80, 0.65, 1.0, 0.90))
            Step-by-step Calculation:
            1. Collection (FC): 80.0%
            2. After Competition: 80.0% × (1 - 65.0%) = 28.0%
            ...
        """
        final = AvailabilityCalculator.calculate(fc, fcp, fs, fl)

        step1 = fc * 100
        step2 = fc * (1 - fcp) * 100
        step3 = fc * (1 - fcp) * fs * 100
        step4 = final

        explanation = f"""
Step-by-step Calculation:
1. Collection (FC): {step1:.1f}%
2. After Competition: {fc:.2f} × (1 - {fcp:.2f}) = {step2:.1f}%
3. After Seasonality: {step2:.1f}% × {fs:.2f} = {step3:.1f}%
4. After Logistics: {step3:.1f}% × {fl:.2f} = {step4:.1f}%

Final Availability: {final:.2f}%
        """.strip()

        return explanation

    @staticmethod
    def validate_factors(
        fc: Optional[float] = None,
        fcp: Optional[float] = None,
        fs: Optional[float] = None,
        fl: Optional[float] = None
    ) -> tuple[bool, list[str]]:
        """
        Validate availability factors.

        Args:
            fc: Collection factor (optional)
            fcp: Competition factor (optional)
            fs: Seasonal factor (optional)
            fl: Logistic factor (optional)

        Returns:
            Tuple of (is_valid, list_of_errors)

        Example:
            >>> calc = AvailabilityCalculator()
            >>> is_valid, errors = calc.validate_factors(fc=1.5, fcp=0.5)
            >>> is_valid
            False
            >>> errors
            ['FC must be between 0 and 1, got 1.5']
        """
        errors = []

        factors = {
            'FC': fc,
            'FCp': fcp,
            'FS': fs,
            'FL': fl
        }

        for name, value in factors.items():
            if value is not None:
                if not isinstance(value, (int, float)):
                    errors.append(f"{name} must be a number, got {type(value).__name__}")
                elif not 0 <= value <= 1:
                    errors.append(f"{name} must be between 0 and 1, got {value}")

        return len(errors) == 0, errors
