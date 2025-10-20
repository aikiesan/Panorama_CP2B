"""
UI Module - Clean UI Components (SOLID Principle)
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Each module has a single responsibility:
- kpi_components: KPI cards and metrics
- filter_components: Filter controls
- selector_components: Sector/residue selectors
- table_components: Data tables and downloads
- card_components: Info and parameter cards
- tabs: Tab rendering (legacy)
- horizontal_nav: Navigation components
"""

# KPI Components
from .kpi_components import (
    render_kpi_cards,
    render_sector_kpis,
    render_comparison_metrics
)

# Filter Components
from .filter_components import (
    render_filters_sidebar,
    render_bmp_range_filter,
    render_residue_search
)

# Selector Components
from .selector_components import (
    render_sector_selector,
    render_residue_selector_for_sector,
    render_full_selector
)

# Phase 5: Culture Hierarchy Selectors (3-Level: Sector -> Culture -> Residue)
from .culture_selector import (
    render_culture_selector,
    render_residue_selector_for_culture
)

from .hierarchical_selector import (
    render_full_selector_3_levels,
    render_quick_selector_with_hierarchy
)

# Table Components
from .table_components import (
    render_data_table,
    render_parameter_ranges_table,
    render_comparison_table
)

# Card Components
from .card_components import (
    render_info_card,
    render_compact_parameter_card,
    render_gradient_card,
    render_status_card,
    show_about_section
)

# Phase 2 Components - New UI Elements
from .availability_card import (
    render_availability_card,
    render_sub_residue_card
)

from .scenario_selector import (
    render_scenario_selector,
    render_scenario_tabs,
    render_scenario_comparison_header,
    render_scenario_info_box,
    render_scenario_selector_simple,
    render_scenario_with_metrics
)

from .contribution_chart import (
    render_contribution_pie_chart,
    render_contribution_bar_chart,
    render_contribution_comparison,
    render_sector_contribution_chart,
    render_sector_bar_chart,
    render_contribution_metrics_row
)

from .municipality_ranking import (
    render_top_municipalities_table,
    render_municipality_bar_chart,
    render_municipality_pie_chart,
    render_municipality_metrics,
    render_municipality_comparison,
    render_municipality_detail_card,
    render_municipality_distribution_map_placeholder
)

from .validation_panel import (
    render_data_validation,
    render_validation_summary,
    render_data_source_info,
    render_data_quality_summary
)

# Legacy/Existing Components
from .tabs import render_sector_tabs
from .main_navigation import (
    render_main_navigation,
    render_sidebar_navigation,
    render_navigation_divider
)

__all__ = [
    # KPI
    'render_kpi_cards',
    'render_sector_kpis',
    'render_comparison_metrics',

    # Filters
    'render_filters_sidebar',
    'render_bmp_range_filter',
    'render_residue_search',

    # Selectors
    'render_sector_selector',
    'render_residue_selector_for_sector',
    'render_full_selector',

    # Phase 5: Culture Hierarchy (3-Level)
    'render_culture_selector',
    'render_residue_selector_for_culture',
    'render_full_selector_3_levels',
    'render_quick_selector_with_hierarchy',

    # Tables
    'render_data_table',
    'render_parameter_ranges_table',
    'render_comparison_table',

    # Cards
    'render_info_card',
    'render_compact_parameter_card',
    'render_gradient_card',
    'render_status_card',
    'show_about_section',

    # Phase 2: Availability Card
    'render_availability_card',
    'render_sub_residue_card',

    # Phase 2: Scenario Selector
    'render_scenario_selector',
    'render_scenario_tabs',
    'render_scenario_comparison_header',
    'render_scenario_info_box',
    'render_scenario_selector_simple',
    'render_scenario_with_metrics',

    # Phase 2: Contribution Charts
    'render_contribution_pie_chart',
    'render_contribution_bar_chart',
    'render_contribution_comparison',
    'render_sector_contribution_chart',
    'render_sector_bar_chart',
    'render_contribution_metrics_row',

    # Phase 2: Municipality Ranking
    'render_top_municipalities_table',
    'render_municipality_bar_chart',
    'render_municipality_pie_chart',
    'render_municipality_metrics',
    'render_municipality_comparison',
    'render_municipality_detail_card',
    'render_municipality_distribution_map_placeholder',

    # Phase 2: Validation Panel
    'render_data_validation',
    'render_validation_summary',
    'render_data_source_info',
    'render_data_quality_summary',

    # Legacy
    'render_sector_tabs',

    # Navigation
    'render_main_navigation',
    'render_sidebar_navigation',
    'render_navigation_divider',
]
