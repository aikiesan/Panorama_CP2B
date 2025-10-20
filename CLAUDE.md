# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**PanoramaCP2B** is a Streamlit-based research platform for biogas and bio-product research at UNICAMP. It provides:
- Laboratory validation tools for biogas research
- Scientific data comparison with literature values
- Database of residue characteristics and availability factors
- Multi-sector analysis (Agricultural, Livestock, Urban residues)

**Current Status**: Active Phase 5 (SAF Validation & Hierarchical Database Restructuring)

---

## Core Architecture

### High-Level Structure

```
PanoramaCP2B/
├── app.py                          # Main Streamlit entry point (homepage)
├── pages/                          # Multi-page Streamlit application
│   ├── 1_📊_Disponibilidade.py     # Availability factors & scenarios
│   ├── 2_🧪_Parametros_Quimicos.py # Chemical parameters & validation
│   ├── 3_📚_Referencias_Cientificas.py # Scientific references
│   ├── 4_🔬_Comparacao_Laboratorial.py # Lab comparison tool
│   ├── 3_📈_Análise_Comparativa.py # Comparative analysis
│   └── 4_🏭_Análise_de_Setores.py  # Sector analysis
├── src/
│   ├── models/
│   │   └── residue_models.py       # Core dataclasses (ParameterRange, ChemicalParameters, ResidueData)
│   ├── services/                   # Business logic layer (SOLID SRP)
│   │   ├── availability_calculator.py # SAF calculation engine
│   │   ├── scenario_manager.py     # Scenario handling
│   │   └── contribution_analyzer.py # Sector contribution analysis
│   ├── ui/                         # UI component library
│   │   ├── card_components.py
│   │   ├── filter_components.py
│   │   ├── selector_components.py
│   │   ├── table_components.py
│   │   ├── kpi_components.py
│   │   ├── municipality_ranking.py
│   │   ├── availability_card.py
│   │   └── scenario_selector.py
│   ├── data/                       # Data definitions (no business logic)
│   │   ├── residue_registry.py    # Master residue catalog
│   │   ├── phase_5_saf_data.py    # SAF validation data for all residues
│   │   ├── cp2b_macrodata.py      # Macro-level production data
│   │   ├── cp2b_culturas.py       # Culture definitions
│   │   ├── agricultura/           # 22 agricultural residue definitions
│   │   ├── pecuaria/              # 7 livestock residue definitions
│   │   ├── urbano/                # 4 urban residue definitions
│   │   └── industrial/            # 5 industrial residue definitions
│   ├── data_sources/              # External data handlers
│   │   ├── sidra_handler.py       # IBGE agricultural data
│   │   ├── mapbiomas_handler.py   # Land use/cover data
│   │   ├── agro_handler.py        # Agricultural statistics
│   │   ├── lab_data_handler.py    # Laboratory data processing
│   │   └── socioeco_handler.py    # Socioeconomic data
│   ├── data_handler.py            # SQLite database layer (@st.cache_data)
│   ├── plotter.py                 # Plotly chart creation
│   ├── plotly_theme.py            # Plotly theming
│   └── utils/
│       ├── formatters.py          # Display formatting
│       ├── validators.py          # Data validation
│       ├── csv_importer.py        # CSV import utilities
│       └── saf_helpers.py         # SAF calculation helpers
├── data/
│   ├── cp2b_maps.db               # SQLite database
│   └── processed/
│       └── sp_municipios_simplified_0_001.geojson
├── assets/
│   └── styles.css                 # Streamlit CSS customization
└── requirements.txt
```

### Design Principles

The codebase follows **SOLID principles**, particularly:

- **S (Single Responsibility)**: Each module has one clear purpose
  - `data_handler.py` - Database operations only
  - `availability_calculator.py` - SAF math only
  - `residue_models.py` - Data structures only

- **D (Dependency Inversion)**: Business logic is independent
  - Services receive data models
  - UI components receive calculated data
  - Easy to test and refactor

### Key Data Models

**ResidueData** (src/models/residue_models.py): Represents a single residue with:
- Basic metadata: name, sector, culture_group
- Chemical parameters: BMP, TS, VS, C:N ratio, pH, etc.
- Availability factors: FC, FCp, FS, FL (for SAF calculation)
- Literature references and priority tier
- Phase 5 SAF validation fields

**ParameterRange**: Stores MIN/MEAN/MAX values for comparison:
- Used for literature validation ranges
- Supports display formatting and range checking

---

## Running the Application

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Development

```bash
# Run the main app (homepage)
streamlit run app.py

# Run a specific page
streamlit run pages/1_📊_Disponibilidade.py

# Access at: http://localhost:8501
```

### Key Streamlit Features

- **@st.cache_data**: Used in data_handler.py for database queries (TTL: 3600s)
- **Session state**: Manages user selections across page refreshes
- **st.columns()**: Layout containers for responsive design
- **Plotly integration**: Interactive charts with custom theme

---

## Database

**Location**: `data/cp2b_maps.db` (SQLite)

**Key Tables**:
- `municipalities` - Municipality-level biogas potential
- `residues` - ResidueData entries (now hierarchical by culture)
- `chemical_parameters` - Detailed parameter ranges from literature
- `references` - Scientific citations with DOI

**Current Phase 5 Work**:
- Reorganizing residues hierarchically by culture (removing duplicates)
- Applying SAF validation data to 26/39 residues (67% complete)
- Adding parent_residue field for composite residues

---

## Development Workflow

### Common Tasks

#### Adding a New Residue

1. Create definition file in appropriate sector folder:
   ```python
   # src/data/agricultura/new_residue.py
   from src.models.residue_models import ResidueData, ChemicalParameters, ParameterRange

   NEW_RESIDUE = ResidueData(
       name="New Residue Name",
       sector="Agrícola",
       culture_group="Culture Name",
       # ... other fields
   )
   ```

2. Register in residue_registry.py:
   ```python
   from src.data.agricultura.new_residue import NEW_RESIDUE

   RESIDUE_REGISTRY = {
       # ... existing
       "new_residue_key": NEW_RESIDUE,
   }
   ```

3. Apply SAF data if available (Phase 5):
   ```python
   # In src/data/phase_5_saf_data.py
   from src.utils.saf_helpers import apply_saf_to_residue

   residue = RESIDUE_REGISTRY["new_residue_key"]
   apply_saf_to_residue(residue, "New Residue Name")
   ```

#### Adding a New Page

1. Create file in `pages/` with naming convention: `number_emoji_page_name.py`
2. Streamlit auto-discovers pages in alphabetical order
3. Import UI components from `src/ui/`:
   ```python
   import streamlit as st
   from src.ui.selector_components import render_residue_selector
   from src.data_handler import load_residues

   st.set_page_config(page_title="...", layout="wide")

   residues = load_residues()
   selected_residue = render_residue_selector(residues)
   # ... rest of page
   ```

#### Modifying Chemical Parameters

Parameters are defined as `ParameterRange` objects in residue dataclasses:

```python
# In src/data/agricultura/residue_file.py
ChemicalParameters(
    bmp=250,
    bmp_unit="ml CH₄/g VS",
    ts=10.5,
    vs=8.2,
    vs_basis="TS",
    # Add ranges from literature:
    bmp_range=ParameterRange(
        min=200, mean=250, max=300, unit="ml CH₄/g VS"
    ),
    # ... other ranges
)
```

#### Calculating Availability (SAF)

Use the AvailabilityCalculator service:

```python
from src.services.availability_calculator import AvailabilityCalculator

calc = AvailabilityCalculator()
availability = calc.calculate(
    fc=0.80,   # Collection factor
    fcp=0.65,  # Competition factor
    fs=1.0,    # Seasonal factor
    fl=0.90    # Logistic factor
)
# Returns: percentage (0-100)
```

---

## Critical Files for Context

### Data Definition Phase 5
- **src/data/phase_5_saf_data.py** - Complete SAF validation mapping for all 29 residues
- **src/data/residue_registry.py** - Master catalog of all residues
- **PHASE_5_PROGRESS_REPORT.md** - Latest status on Phase 5 completion

### Architecture Documentation
- **PAGE_ARCHITECTURE.md** - UI page structure and data flow
- **DATABASE_ARCHITECTURE_COMPLETE.md** - Database schema and relationships
- **INTEGRATION_PLAN.md** - Integration strategy for new features

### Recent Work
- Phase 5 focuses on SAF validation and hierarchical reorganization
- Major recent changes: Database restructuring, SAF data infrastructure, Phase 5 completeness audit

---

## Caching Strategy

Performance optimization uses Streamlit's caching:

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_all_municipalities():
    # Database query - expensive
    engine = get_db_connection()
    df = pd.read_sql("SELECT * FROM municipalities", engine)
    return df
```

**Key cached functions**:
- `load_all_municipalities()` - Loads all municipality data
- `load_residues()` - Loads residue catalog
- `get_db_connection()` - Database engine creation

---

## Code Style & Standards

### Type Hints
Use type hints for all functions (enforced in services layer):

```python
def calculate(self, fc: float, fcp: float, fs: float, fl: float) -> float:
    """Docstring with Args and Returns"""
    pass
```

### Docstrings
Required for all public functions:
```python
def my_function(param: str) -> bool:
    """
    Short description.

    Args:
        param: Description of parameter

    Returns:
        Description of return value

    Raises:
        ValueError: When this error occurs
    """
```

### Directory Organization
- **No circular imports** - UI → Services → Models → Data
- **Dataclasses in models/** - Pure data structures, no logic
- **Services/** - Business logic (SAF calculations, analysis)
- **UI/** - Streamlit component library
- **Data/** - Data definitions and source handlers

---

## References & Research

### Key Scientific Papers
- Base methodology: 15+ peer-reviewed papers on residue characterization
- SAF methodology: Validated through UNICAMP CP2B research group
- Geographic data: MapBiomas (land use), IBGE/SIDRA (production), SEAPA (livestock)

### SAF Components
- **FC (Collection Factor)**: Technical efficiency (0.55-0.95)
- **FCp (Competition Factor)**: Market competition for alternative uses
- **FS (Seasonality Factor)**: Variation through year (0.70-1.0)
- **FL (Logistic Factor)**: Distance-based economic restriction (0.65-1.0)

Formula: **D_final = FC × (1 - FCp) × FS × FL × 100%**

---

## Common Issues & Solutions

### Database Connection Errors
- Ensure `data/cp2b_maps.db` exists
- Check database path in secrets: `st.secrets["database"]["path"]`
- Use absolute path conversion in get_db_connection()

### Streamlit Cache Invalidation
- Cache TTL: 3600 seconds (1 hour)
- To force refresh: Restart Streamlit app or modify cached function
- Session state persists across reruns

### Import Errors
- Ensure all sector folders have `__init__.py`
- Check residue is registered in residue_registry.py
- Verify relative imports use absolute paths from project root

---

## Testing & Quality

Currently no automated tests. Manual testing workflow:
1. Run Streamlit app locally
2. Test each page for user interactions
3. Verify database queries work
4. Check chart rendering with different data

For Phase 5 work, validate SAF calculations match expected ranges before committing.

---

## Recent Git History

Recent significant changes (last 6 commits):
1. Phase 5 completeness audit script
2. Vinhaça availability factors correction (data quality)
3. Phase 5 data quality fixes (sector organization)
4. Phase 5 SAF batch application (26/39 residues = 67%)
5. Phase 5 SAF Validation & Infrastructure (50% complete)
6. CP2B macro data loader for Jupyter integration

All commits follow pattern: `type: Description (scope if needed)`

---

## Contact & Documentation

- **Primary Team**: CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos), UNICAMP
- **Latest Update**: October 2024
- **Version**: 1.0 Prototype (Active development)

For architectural questions, check PHASE_5_PROGRESS_REPORT.md and PAGE_ARCHITECTURE.md.
