"""
Data Sources Module
Specialized handlers for different data sources following Single Responsibility Principle.
"""

from .sidra_handler import *
from .mapbiomas_handler import *
from .agro_handler import *
from .socioeco_handler import *
from .lab_data_handler import *

__all__ = [
    'load_sidra_data',
    'load_mapbiomas_data',
    'load_agro_data',
    'load_socioeco_data',
    'load_lab_data',
]
