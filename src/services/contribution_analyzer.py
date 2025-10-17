"""
Contribution Analyzer Service
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Analyze contributions of sub-residues and rank municipalities.
Provides insights on: % contribution breakdown, municipality ranking, sector aggregation.

SOLID Compliance:
- Single Responsibility: Only analyzes contributions and rankings
- Open/Closed: Easy to add new analysis types without modifying existing code
- Liskov Substitution: Compatible data structures with existing models
- Interface Segregation: Focused methods for specific analysis tasks
- Dependency Inversion: Depends on ResidueData abstractions, not implementation
"""

from typing import List, Dict, Optional
from src.models.residue_models import ResidueData


class ContributionAnalyzer:
    """
    Analyze contributions of sub-residues and rank municipalities.

    Provides three main analysis capabilities:
    1. Calculate % contribution of each sub-residue to total
    2. Rank municipalities by CH4 potential
    3. Aggregate totals by sector (Agricultura, Pecuária, Urbano, Industrial)

    All analysis is purely data-driven, no UI coupling.

    Example:
        >>> analyzer = ContributionAnalyzer()
        >>> contributions = analyzer.calculate_contributions([palha, bagaco, vinhaca])
        >>> municipalities = analyzer.rank_municipalities(residue_data, top_n=10)
    """

    @staticmethod
    def calculate_contributions(
        residue_list: List[ResidueData],
        scenario: str = 'Realista'
    ) -> List[Dict[str, any]]:
        """
        Calculate percentage contribution of each residue to total.

        Analyzes how much each sub-residue contributes to the total CH4 potential.
        Useful for understanding which components dominate overall potential.

        Args:
            residue_list: List of ResidueData objects (typically sub-residues)
            scenario: Which scenario to analyze ('Pessimista', 'Realista', 'Otimista', 'Teórico')

        Returns:
            List of dictionaries, each containing:
                {
                    'name': str,            # Residue name
                    'ch4': float,           # CH4 potential for scenario
                    'percentage': float,    # % contribution to total
                    'icon': str,           # Emoji icon
                    'rank': int            # Rank by CH4 potential (1-indexed)
                }
            Sorted by CH4 potential (descending)

        Example:
            >>> contributions = ContributionAnalyzer.calculate_contributions(
            ...     [BAGACO_DATA, PALHA_DATA, VINHACA_DATA],
            ...     scenario='Realista'
            ... )
            >>> contributions
            [
                {'name': 'Palha', 'ch4': 5620.0, 'percentage': 92.4, 'icon': '🌾', 'rank': 1},
                {'name': 'Torta', 'ch4': 310.0, 'percentage': 5.1, 'icon': '📦', 'rank': 2},
                {'name': 'Vinhaça', 'ch4': 150.0, 'percentage': 2.5, 'icon': '💧', 'rank': 3}
            ]
        """
        if not residue_list:
            return []

        # Collect CH4 potentials for the specified scenario
        results = []
        for residue in residue_list:
            ch4_potential = residue.scenarios.get(scenario, 0.0)
            results.append({
                'name': residue.name,
                'ch4': ch4_potential,
                'icon': residue.icon,
                'category': residue.category
            })

        # Calculate total
        total_ch4 = sum(r['ch4'] for r in results)

        if total_ch4 == 0:
            # All zeros - assign 0% to all
            for result in results:
                result['percentage'] = 0.0
        else:
            # Calculate percentages
            for result in results:
                result['percentage'] = round((result['ch4'] / total_ch4) * 100, 2)

        # Sort by CH4 potential (descending) and add ranks
        results.sort(key=lambda x: x['ch4'], reverse=True)
        for rank, result in enumerate(results, start=1):
            result['rank'] = rank

        return results

    @staticmethod
    def rank_municipalities(
        residue_data: ResidueData,
        top_n: int = 10,
        scenario: str = 'Realista'
    ) -> List[Dict[str, any]]:
        """
        Rank top N municipalities by CH4 potential.

        Sorts municipalities by their biogas generation potential and provides
        ranking with CH4 volume and equivalent electricity generation.

        Args:
            residue_data: ResidueData object with top_municipalities data
            top_n: Number of top municipalities to return (default: 10)
            scenario: Which scenario to use (default: 'Realista')

        Returns:
            List of dictionaries (top N municipalities), each containing:
                {
                    'rank': int,            # 1-indexed rank
                    'name': str,           # Municipality name
                    'ch4': float,          # CH4 potential (m³ or ton)
                    'electricity': float,  # Equivalent electricity (GWh)
                    'percentage': float    # % of top 10 total
                }

        Example:
            >>> municipalities = ContributionAnalyzer.rank_municipalities(
            ...     cana_data,
            ...     top_n=10
            ... )
            >>> municipalities[0]
            {
                'rank': 1,
                'name': 'Sertãozinho',
                'ch4': 120.5,
                'electricity': 172.3,
                'percentage': 15.2
            }
        """
        if not residue_data.top_municipalities:
            return []

        # Create list with CH4 potentials
        municipalities = []
        for munic_data in residue_data.top_municipalities:
            ch4_potential = munic_data.get('ch4_potential', 0.0)
            municipalities.append({
                'name': munic_data.get('name', 'Unknown'),
                'ch4': ch4_potential,
                'electricity': munic_data.get('electricity_potential', 0.0),
                'state': munic_data.get('state'),
                'production': munic_data.get('production', 0.0)
            })

        # Sort by CH4 potential (descending)
        municipalities.sort(key=lambda x: x['ch4'], reverse=True)

        # Get top N
        top_municipalities = municipalities[:top_n]

        # Calculate percentage of total top 10
        total_ch4 = sum(m['ch4'] for m in top_municipalities)

        results = []
        for rank, munic in enumerate(top_municipalities, start=1):
            percentage = (munic['ch4'] / total_ch4 * 100) if total_ch4 > 0 else 0.0
            results.append({
                'rank': rank,
                'name': munic['name'],
                'ch4': round(munic['ch4'], 2),
                'electricity': round(munic['electricity'], 2),
                'percentage': round(percentage, 2),
                'state': munic.get('state'),
                'production': munic.get('production')
            })

        return results

    @staticmethod
    def aggregate_by_sector(
        all_residues: Dict[str, List[ResidueData]],
        scenario: str = 'Realista'
    ) -> Dict[str, Dict[str, float]]:
        """
        Aggregate CH4 totals and availability by sector.

        Summarizes all residues grouped by sector, showing:
        - Total CH4 potential per sector
        - Count of residues per sector
        - Average availability per sector

        Args:
            all_residues: Dictionary mapping sector names to lists of ResidueData
                Format: {
                    'Agricultura': [palha_data, bagaco_data, ...],
                    'Pecuária': [bovinos_data, ...],
                    'Urbano': [rsu_data, ...],
                    'Industrial': [soro_queijo_data, ...]
                }
            scenario: Which scenario to aggregate ('Realista' default)

        Returns:
            Dictionary with sector totals:
                {
                    'Agricultura': {
                        'total_ch4': 15000.0,
                        'residue_count': 7,
                        'avg_availability': 32.5,
                        'residues': [...]  # List of residues in sector
                    },
                    ...
                }

        Example:
            >>> sectors = {
            ...     'Agricultura': [palha, bagaco, vinhaça],
            ...     'Pecuária': [bovinos, suinos],
            ...     'Urbano': [rsu]
            ... }
            >>> aggregated = ContributionAnalyzer.aggregate_by_sector(sectors)
            >>> aggregated['Agricultura']['total_ch4']
            15234.5
        """
        aggregation = {}

        for sector_name, residues in all_residues.items():
            if not residues:
                continue

            # Calculate totals
            total_ch4 = 0.0
            total_availability = 0.0
            residue_count = 0

            residue_details = []

            for residue in residues:
                ch4_potential = residue.scenarios.get(scenario, 0.0)
                total_ch4 += ch4_potential
                total_availability += residue.availability.final_availability
                residue_count += 1

                residue_details.append({
                    'name': residue.name,
                    'ch4': ch4_potential,
                    'availability': residue.availability.final_availability,
                    'icon': residue.icon
                })

            # Calculate averages
            avg_availability = (total_availability / residue_count) if residue_count > 0 else 0.0

            aggregation[sector_name] = {
                'total_ch4': round(total_ch4, 2),
                'residue_count': residue_count,
                'avg_availability': round(avg_availability, 2),
                'residues': residue_details,
                'scenario': scenario
            }

        return aggregation

    @staticmethod
    def calculate_sector_percentages(
        sector_aggregation: Dict[str, Dict[str, float]]
    ) -> Dict[str, float]:
        """
        Calculate percentage contribution of each sector to total CH4.

        Helper method to determine sector importance in overall potential.

        Args:
            sector_aggregation: Output from aggregate_by_sector()

        Returns:
            Dictionary mapping sector names to their % of total:
                {
                    'Agricultura': 45.3,
                    'Pecuária': 30.1,
                    'Urbano': 15.2,
                    'Industrial': 9.4
                }

        Example:
            >>> percentages = ContributionAnalyzer.calculate_sector_percentages(
            ...     sector_agg
            ... )
            >>> percentages['Agricultura']
            45.3
        """
        # Calculate total CH4 across all sectors
        total_ch4 = sum(s['total_ch4'] for s in sector_aggregation.values())

        if total_ch4 == 0:
            return {sector: 0.0 for sector in sector_aggregation.keys()}

        # Calculate percentages
        percentages = {}
        for sector_name, data in sector_aggregation.items():
            pct = (data['total_ch4'] / total_ch4) * 100
            percentages[sector_name] = round(pct, 2)

        return percentages

    @staticmethod
    def find_top_contributor(
        residue_list: List[ResidueData],
        scenario: str = 'Realista'
    ) -> Optional[Dict[str, any]]:
        """
        Find the residue with highest CH4 potential.

        Quick lookup for the most significant contributor to potential.

        Args:
            residue_list: List of ResidueData objects
            scenario: Which scenario to analyze

        Returns:
            Dictionary with top residue data or None if list is empty:
                {
                    'name': str,
                    'ch4': float,
                    'percentage': float,  # Of total list
                    'icon': str
                }

        Example:
            >>> top = ContributionAnalyzer.find_top_contributor(
            ...     [palha, bagaco, vinhaca]
            ... )
            >>> top['name']
            'Palha de Cana-de-açúcar'
        """
        if not residue_list:
            return None

        contributions = ContributionAnalyzer.calculate_contributions(
            residue_list,
            scenario
        )

        if not contributions:
            return None

        return contributions[0]  # Already sorted by CH4 (descending)
