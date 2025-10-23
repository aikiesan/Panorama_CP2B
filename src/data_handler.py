"""
Data Handler Module - Single Responsibility Principle
Handles all data access and processing operations for the biogas dashboard.
"""

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path


def get_db_connection(db_type="municipalities"):
    """
    Returns SQLAlchemy engine using database path from Streamlit secrets or default paths.

    Handles both local development (with secrets.toml) and Streamlit Cloud deployment
    (without secrets, using default committed database files).

    Args:
        db_type: Type of database - "municipalities" or "residues"

    Returns:
        sqlalchemy.engine.Engine: Database connection engine
    """
    # Default database paths (used when secrets don't exist - e.g., Streamlit Cloud)
    DEFAULT_PATHS = {
        "municipalities": "data/cp2b_maps.db",
        "residues": "data/cp2b_panorama.db"  # ✅ Canonical path (consolidated from webapp/)
    }

    db_path = None

    # Try to get path from secrets (local development)
    try:
        if "database" in st.secrets:
            # Support legacy "path" key for backward compatibility
            if "path" in st.secrets["database"]:
                db_path = st.secrets["database"]["path"]
            elif db_type == "residues":
                db_path = st.secrets["database"]["residues_db"]
            else:
                db_path = st.secrets["database"]["municipalities_db"]
    except (KeyError, FileNotFoundError):
        # Secrets don't exist - use default paths (Streamlit Cloud deployment)
        pass

    # Fallback to default paths if secrets weren't found
    if db_path is None:
        db_path = DEFAULT_PATHS.get(db_type, DEFAULT_PATHS["municipalities"])

    # Convert to absolute path if relative
    if not Path(db_path).is_absolute():
        db_path = Path(__file__).parent.parent / db_path

    engine = create_engine(f"sqlite:///{db_path}")
    return engine


def get_residue_db_connection():
    """Returns connection to residue database (panorama_cp2b_final.db)"""
    return get_db_connection("residues")


def get_municipality_db_connection():
    """Returns connection to municipality database (cp2b_maps.db)"""
    return get_db_connection("municipalities")


@st.cache_data(ttl=3600)
def load_all_municipalities():
    """
    Loads all municipality data from the database.
    Cached for 1 hour to prevent redundant database queries.
    
    Returns:
        pd.DataFrame: Complete municipalities dataset
    """
    engine = get_db_connection()
    query = "SELECT * FROM municipalities"
    df = pd.read_sql(query, engine)
    
    # Ensure numeric columns are properly typed
    numeric_cols = [
        'area_km2', 'populacao_2022', 'rsu_potencial_m_ano', 'rpo_potencial_m_ano',
        'biogas_cana_m_ano', 'biogas_soja_m_ano', 'biogas_milho_m_ano',
        'biogas_bovinos_m_ano', 'biogas_cafe_m_ano', 'biogas_citros_m_ano',
        'biogas_suino_m_ano', 'biogas_aves_m_ano', 'biogas_piscicultura_m_ano',
        'biogas_silvicultura_m_ano', 'total_final_m_ano', 'total_agricola_m_ano',
        'total_pecuaria_m_ano', 'total_urbano_m_ano', 'lat', 'lon', 'densidade_demografica'
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df


@st.cache_data
def get_kpis_totais(_df: pd.DataFrame) -> dict:
    """
    Calculates state-wide KPIs from filtered DataFrame.
    
    Args:
        _df: Filtered municipality DataFrame
        
    Returns:
        dict: Dictionary with total biogas, municipalities count, and sector breakdowns
    """
    total_biogas = _df['total_final_m_ano'].sum()
    total_municipios = len(_df)
    total_agricola = _df['total_agricola_m_ano'].sum()
    total_pecuaria = _df['total_pecuaria_m_ano'].sum()
    total_urbano = _df['total_urbano_m_ano'].sum()
    
    # Find top municipality
    top_mun_idx = _df['total_final_m_ano'].idxmax()
    top_municipio = _df.loc[top_mun_idx, 'nome_municipio'] if not _df.empty else "N/A"
    top_municipio_valor = _df.loc[top_mun_idx, 'total_final_m_ano'] if not _df.empty else 0
    
    return {
        "total_biogas": total_biogas,
        "total_municipios": total_municipios,
        "total_agricola": total_agricola,
        "total_pecuaria": total_pecuaria,
        "total_urbano": total_urbano,
        "top_municipio": top_municipio,
        "top_municipio_valor": top_municipio_valor
    }


@st.cache_data
def get_volume_por_setor(_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates biogas volume by sector (Agriculture, Livestock, Urban).
    
    Args:
        _df: Municipality DataFrame
        
    Returns:
        pd.DataFrame: Aggregated data with columns ['setor', 'volume']
    """
    setores = {
        'Agricultura': _df['total_agricola_m_ano'].sum(),
        'Pecuária': _df['total_pecuaria_m_ano'].sum(),
        'Urbano': _df['total_urbano_m_ano'].sum()
    }
    
    df_setor = pd.DataFrame(list(setores.items()), columns=['setor', 'volume'])
    return df_setor


@st.cache_data
def get_volume_por_substrato(_df: pd.DataFrame) -> pd.DataFrame:
    """
    Breaks down biogas volume by specific substrate type.
    
    Args:
        _df: Municipality DataFrame
        
    Returns:
        pd.DataFrame: Substrate breakdown with columns ['substrato', 'volume']
    """
    substratos = {
        'Cana-de-açúcar': _df['biogas_cana_m_ano'].sum(),
        'Soja': _df['biogas_soja_m_ano'].sum(),
        'Milho': _df['biogas_milho_m_ano'].sum(),
        'Café': _df['biogas_cafe_m_ano'].sum(),
        'Citros': _df['biogas_citros_m_ano'].sum(),
        'Bovinos': _df['biogas_bovinos_m_ano'].sum(),
        'Suínos': _df['biogas_suino_m_ano'].sum(),
        'Aves': _df['biogas_aves_m_ano'].sum(),
        'Piscicultura': _df['biogas_piscicultura_m_ano'].sum(),
        'Silvicultura': _df['biogas_silvicultura_m_ano'].sum(),
        'RSU': _df['rsu_potencial_m_ano'].sum(),
        'RPO': _df['rpo_potencial_m_ano'].sum()
    }
    
    df_substrato = pd.DataFrame(list(substratos.items()), columns=['substrato', 'volume'])
    # Sort by volume descending and filter out zero values
    df_substrato = df_substrato[df_substrato['volume'] > 0].sort_values('volume', ascending=False)
    return df_substrato


@st.cache_data
def get_top_municipios(_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Returns top N municipalities by total biogas potential.
    
    Args:
        _df: Municipality DataFrame
        n: Number of top municipalities to return
        
    Returns:
        pd.DataFrame: Top municipalities with relevant columns
    """
    df_top = _df.nlargest(n, 'total_final_m_ano')[
        ['nome_municipio', 'total_final_m_ano', 'total_agricola_m_ano', 
         'total_pecuaria_m_ano', 'total_urbano_m_ano', 'populacao_2022']
    ].copy()
    
    return df_top


def filter_dataframe(df: pd.DataFrame, **filters) -> pd.DataFrame:
    """
    Applies dynamic filters to the dataframe.
    
    Args:
        df: Source DataFrame
        **filters: Keyword arguments for filtering
            - municipios: list of municipality names
            - categorias: list of potential categories
            - pop_range: tuple (min, max) population
            - setores: list of sectors to include
            
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    df_filtered = df.copy()
    
    # Filter by municipalities
    if 'municipios' in filters and filters['municipios']:
        df_filtered = df_filtered[df_filtered['nome_municipio'].isin(filters['municipios'])]
    
    # Filter by potential category
    if 'categorias' in filters and filters['categorias']:
        df_filtered = df_filtered[df_filtered['categoria_potencial'].isin(filters['categorias'])]
    
    # Filter by population range
    if 'pop_range' in filters and filters['pop_range']:
        min_pop, max_pop = filters['pop_range']
        df_filtered = df_filtered[
            (df_filtered['populacao_2022'] >= min_pop) & 
            (df_filtered['populacao_2022'] <= max_pop)
        ]
    
    # Filter by sector (requires at least one sector to have volume > 0)
    if 'setores' in filters and filters['setores']:
        mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
        if 'Agricultura' in filters['setores']:
            mask |= df_filtered['total_agricola_m_ano'] > 0
        if 'Pecuária' in filters['setores']:
            mask |= df_filtered['total_pecuaria_m_ano'] > 0
        if 'Urbano' in filters['setores']:
            mask |= df_filtered['total_urbano_m_ano'] > 0
        df_filtered = df_filtered[mask]
    
    return df_filtered


@st.cache_data
def get_municipality_details(nome_municipio: str) -> pd.Series:
    """
    Gets detailed data for a specific municipality.

    Args:
        nome_municipio: Name of the municipality

    Returns:
        pd.Series: Municipality data
    """
    df = load_all_municipalities()
    mun_data = df[df['nome_municipio'] == nome_municipio].iloc[0]
    return mun_data


# ============================================================================
# RESIDUE DATA LOADING (from panorama_cp2b_final.db)
# ============================================================================

@st.cache_data(ttl=3600, show_spinner="Carregando resíduos...")
def load_all_residues():
    """
    Load all residues from the residue database.

    Returns:
        pd.DataFrame: All residues with basic metadata including chemical composition
    """
    engine = get_residue_db_connection()
    query = "SELECT * FROM residuos"
    df = pd.read_sql(query, engine)
    return df


@st.cache_data(ttl=3600)
def load_residues_by_sector(sector_code: str = None):
    """
    Load residues filtered by sector.

    Args:
        sector_code: Sector code (AG_AGRICULTURA, PC_PECUARIA, UR_URBANO, IN_INDUSTRIAL)
                     If None, returns all residues grouped by sector

    Returns:
        pd.DataFrame: Filtered residues
    """
    engine = get_residue_db_connection()

    if sector_code:
        query = f"SELECT * FROM residuos WHERE setor = '{sector_code}'"
    else:
        query = "SELECT * FROM residuos ORDER BY setor, nome"

    df = pd.read_sql(query, engine)
    return df


@st.cache_data(ttl=3600)
def load_chemical_parameters(residue_id: int = None):
    """
    Load chemical parameters for residues.

    Args:
        residue_id: Specific residue ID, or None for all

    Returns:
        pd.DataFrame: Chemical parameters
    """
    engine = get_residue_db_connection()

    if residue_id:
        query = f"SELECT * FROM parametros_quimicos WHERE residuo_id = {residue_id}"
    else:
        query = "SELECT * FROM parametros_quimicos"

    df = pd.read_sql(query, engine)
    return df


@st.cache_data(ttl=3600)
def load_availability_factors(residue_id: int = None):
    """
    Load availability factors for residues.

    Args:
        residue_id: Specific residue ID, or None for all

    Returns:
        pd.DataFrame: Availability factors (FDE)
    """
    engine = get_residue_db_connection()

    if residue_id:
        query = f"SELECT * FROM fatores_disponibilidade WHERE residuo_id = {residue_id}"
    else:
        query = "SELECT * FROM fatores_disponibilidade"

    df = pd.read_sql(query, engine)
    return df


@st.cache_data(ttl=3600)
def get_residue_complete_data(residue_nome: str):
    """
    Get complete data for a specific residue (residue + parameters + factors).

    Args:
        residue_nome: Name of the residue

    Returns:
        dict: Complete residue data with all parameters
    """
    engine = get_residue_db_connection()

    # Load residue basic data
    residue_query = f"SELECT * FROM residuos WHERE nome = '{residue_nome}'"
    residue = pd.read_sql(residue_query, engine)

    if residue.empty:
        return None

    residue_id = residue['id'].iloc[0]

    # Load chemical parameters
    chem_params = load_chemical_parameters(residue_id)

    # Load availability factors
    avail_factors = load_availability_factors(residue_id)

    return {
        'residue': residue.iloc[0].to_dict(),
        'chemical_params': chem_params.iloc[0].to_dict() if not chem_params.empty else {},
        'availability': avail_factors.iloc[0].to_dict() if not avail_factors.empty else {}
    }


def map_sector_code_to_name(sector_code: str) -> str:
    """Map database sector codes to friendly names."""
    mapping = {
        'AG_AGRICULTURA': 'Agrícola',
        'PC_PECUARIA': 'Pecuária',
        'UR_URBANO': 'Urbano',
        'IN_INDUSTRIAL': 'Industrial'
    }
    return mapping.get(sector_code, sector_code)


# ============================================================================
# ENHANCED RESIDUE DATA LOADING (Phase 1.1 - Database Integration)
# ============================================================================

@st.cache_data(ttl=3600, show_spinner="Carregando dados dos resíduos...")
def get_all_residues_with_params():
    """
    Load all residues with complete parameters from database.

    Returns complete dataset with:
    - Basic residue info (id, codigo, nome, setor)
    - Chemical parameters (BMP, TS, VS with min/mean/max)
    - Chemical composition (CH4 content, C:N ratio)
    - Availability factors (FC, FCp, FS, FL with min/mean/max)
    - Scenario factors (pessimista, realista, otimista)
    - Literature references and summaries

    Returns:
        pd.DataFrame: Complete residue dataset
    """
    engine = get_residue_db_connection()
    query = "SELECT * FROM residuos"
    df = pd.read_sql(query, engine)

    # Ensure numeric columns are properly typed
    numeric_cols = [
        'bmp_medio', 'bmp_min', 'bmp_max',
        'ts_medio', 'ts_min', 'ts_max',
        'vs_medio', 'vs_min', 'vs_max',
        'fc_medio', 'fc_min', 'fc_max',
        'fcp_medio', 'fcp_min', 'fcp_max',
        'fs_medio', 'fs_min', 'fs_max',
        'fl_medio', 'fl_min', 'fl_max',
        'fator_realista', 'fator_pessimista', 'fator_otimista',
        'chemical_cn_ratio', 'chemical_ch4_content'  # Added CH4 and C:N
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


@st.cache_data(ttl=3600)
def get_sector_summary():
    """
    Get aggregated summary statistics by sector.

    Calculates:
    - Count of residues per sector
    - Average BMP, TS, VS per sector
    - Average availability factors per sector
    - Dominant ranges per sector

    Returns:
        pd.DataFrame: Sector summary statistics
    """
    df = get_all_residues_with_params()

    summary = df.groupby('setor').agg({
        'id': 'count',
        'bmp_medio': ['mean', 'min', 'max', 'std'],
        'ts_medio': ['mean', 'min', 'max', 'std'],
        'vs_medio': ['mean', 'min', 'max', 'std'],
        'fc_medio': 'mean',
        'fcp_medio': 'mean',
        'fs_medio': 'mean',
        'fl_medio': 'mean',
        'fator_realista': 'mean'
    }).round(3)

    # Flatten column names
    summary.columns = ['_'.join(col).strip() for col in summary.columns.values]

    # Rename count column
    summary.rename(columns={'id_count': 'residue_count'}, inplace=True)

    return summary.reset_index()


@st.cache_data(ttl=3600)
def get_bmp_distribution():
    """
    Get BMP distribution data for visualization.

    Returns data optimized for:
    - Box plots
    - Violin plots
    - Histogram analysis

    Returns:
        pd.DataFrame: BMP distribution with sector grouping
    """
    df = get_all_residues_with_params()

    # Create expanded dataset with min/mean/max for distribution
    distribution_data = []

    for _, row in df.iterrows():
        # Add min value
        if pd.notna(row['bmp_min']):
            distribution_data.append({
                'nome': row['nome'],
                'setor': row['setor'],
                'bmp': row['bmp_min'],
                'type': 'min'
            })

        # Add mean value
        if pd.notna(row['bmp_medio']):
            distribution_data.append({
                'nome': row['nome'],
                'setor': row['setor'],
                'bmp': row['bmp_medio'],
                'type': 'mean'
            })

        # Add max value
        if pd.notna(row['bmp_max']):
            distribution_data.append({
                'nome': row['nome'],
                'setor': row['setor'],
                'bmp': row['bmp_max'],
                'type': 'max'
            })

    return pd.DataFrame(distribution_data)


@st.cache_data(ttl=3600)
def get_parameter_correlations():
    """
    Calculate correlation matrix for chemical parameters.

    Returns correlations between:
    - BMP (mean)
    - TS (mean)
    - VS (mean)
    - FC, FCp, FS, FL (availability factors)

    Returns:
        pd.DataFrame: Correlation matrix
    """
    df = get_all_residues_with_params()

    # Select parameters for correlation
    params = [
        'bmp_medio', 'ts_medio', 'vs_medio',
        'fc_medio', 'fcp_medio', 'fs_medio', 'fl_medio'
    ]

    # Calculate correlations
    corr_matrix = df[params].corr()

    # Rename columns/index for display
    display_names = {
        'bmp_medio': 'BMP',
        'ts_medio': 'TS (%)',
        'vs_medio': 'VS (%)',
        'fc_medio': 'FC',
        'fcp_medio': 'FCp',
        'fs_medio': 'FS',
        'fl_medio': 'FL'
    }

    corr_matrix.rename(columns=display_names, index=display_names, inplace=True)

    return corr_matrix


@st.cache_data(ttl=3600)
def get_residue_by_name(residue_name: str):
    """
    Get single residue data by name.

    Args:
        residue_name: Name of the residue

    Returns:
        dict: Complete residue data as dictionary
    """
    df = get_all_residues_with_params()
    residue = df[df['nome'] == residue_name]

    if residue.empty:
        return None

    return residue.iloc[0].to_dict()


def load_residue_from_db(residue_code: str):
    """
    Get single residue data by code (hierarchical selector compatible).

    Args:
        residue_code: Code of the residue (e.g., 'BAGACO', 'VINHACA')

    Returns:
        dict: Complete residue data as dictionary including chemical composition (CH4, C:N)
    """
    df = get_all_residues_with_params()
    residue = df[df['codigo'] == residue_code]

    if residue.empty:
        return None

    return residue.iloc[0].to_dict()


def clear_all_caches():
    """
    Clear all Streamlit caches for data handlers.

    Use this function when database has been updated and you need fresh data.
    """
    get_all_residues_with_params.clear()
    load_all_residues.clear()
    load_all_municipalities.clear()
    get_sector_summary.clear()
    st.cache_data.clear()


@st.cache_data(ttl=3600, show_spinner="Carregando lista de resíduos...")
def get_residues_for_dropdown():
    """
    Get residues formatted for dropdown selector.

    Returns:
        dict: {sector_code: [list of residue names]}
    """
    df = get_all_residues_with_params()

    residues_by_sector = {}

    for sector in df['setor'].unique():
        sector_residues = df[df['setor'] == sector]['nome'].tolist()
        residues_by_sector[sector] = sorted(sector_residues)

    return residues_by_sector


@st.cache_data(ttl=3600)
def calculate_fde(fc: float, fcp: float, fs: float, fl: float) -> float:
    """
    Calculate FDE (Fator de Disponibilidade Efetiva).

    Formula: FDE = FC × FCp × FS × FL × 100%

    IMPORTANT: FCp represents % AVAILABLE after competition (NOT % competing).
    - FCp = 0.70 means 70% available (30% goes to competing uses)
    - FCp = 0.20 means 20% available (80% goes to competing uses like cogeração)

    Args:
        fc: Collection factor (0-1) - Technical collection efficiency
        fcp: Competition factor (0-1) - % AVAILABLE after competing uses
        fs: Seasonality factor (0-1) - Seasonal availability
        fl: Logistic factor (0-1) - Logistic/transport viability

    Returns:
        float: FDE percentage (0-100)

    Examples:
        Bagaço cana (high competition - cogeração):
        - FC=0.95, FCp=0.20 (20% available, 80% to cogeração), FS=0.90, FL=0.90
        - FDE = 0.95 × 0.20 × 0.90 × 0.90 × 100 = 15.4%

        Dejetos suínos (low competition):
        - FC=0.90, FCp=0.75 (75% available), FS=1.0, FL=0.90
        - FDE = 0.90 × 0.75 × 1.0 × 0.90 × 100 = 60.8%
    """
    return fc * fcp * fs * fl * 100.0


# Backward compatibility alias
calculate_saf = calculate_fde


# ============================================================================
# PANORAMA DATABASE ACCESS (Phase 2 - Reference Integration)
# ============================================================================

def get_panorama_connection():
    """
    Get connection to CP2B_Precision_Biogas.db (NEW validated database).

    MIGRATION: Switched from old cp2b_panorama.db to NEW validated database.

    This NEW database contains:
    - 22 validated scientific papers (scientific_papers table)
    - 102 validated chemical parameters (chemical_parameters table)
    - 4 residue types with clean mapping (residue_types table)
    - 15 parameter definitions (parameter_definitions table)

    OLD database had schema mismatches causing serialization errors.
    NEW database has clean schema with simple foreign keys.

    Returns:
        sqlalchemy.engine.Engine: Connection to precision biogas database
    """
    from pathlib import Path

    # NEW VALIDATED DATABASE PATH
    db_path = Path("C:/Users/Lucas/Documents/CP2B/Validacao_dados/CP2B_Precision_Biogas.db")

    if not db_path.exists():
        raise FileNotFoundError(
            f"Precision biogas database not found at: {db_path}\n"
            f"Please ensure the validated database is available."
        )

    engine = create_engine(f"sqlite:///{db_path}")
    return engine


@st.cache_data(ttl=3600)
def _load_residue_id_mapping() -> dict:
    """
    Load residue code → residue_id mapping from NEW precision database.

    This function queries the residue_types table and creates a mapping
    dictionary for quick lookups.

    Returns:
        dict: {residue_code: residue_id, ...}
              e.g., {'CANA_VINHACA': 4, 'SUINO_DEJETO': 3, ...}

    Examples:
        >>> mapping = _load_residue_id_mapping()
        >>> mapping['CANA_VINHACA']
        4
    """
    try:
        conn = get_panorama_connection()

        query = "SELECT residue_id, residue_code FROM residue_types"
        df = pd.read_sql_query(query, conn)

        # Create base mapping from database
        mapping = dict(zip(df['residue_code'], df['residue_id']))

        # Add webapp aliases for backward compatibility
        mapping['VINHACA'] = mapping.get('CANA_VINHACA')  # Legacy
        mapping['DEJETOS_SUINO'] = mapping.get('SUINO_DEJETO')  # Variation
        mapping['CAMA_AVIARIO'] = mapping.get('CAMA_FRANGO')  # Legacy

        return mapping
    except Exception as e:
        st.error(f"Erro ao carregar mapeamento de resíduos: {e}")
        return {}


def _map_residue_code_for_references(residue_codigo: str) -> str:
    """
    DEPRECATED: This function is for OLD database only.

    NEW database uses residue_id mapping via _load_residue_id_mapping().
    Keeping this for backward compatibility but it won't be used.

    Args:
        residue_codigo: Webapp code

    Returns:
        str: Database code (pass-through now)
    """
    # For NEW database, just return as-is
    # The actual mapping happens via residue_id in new functions
    return residue_codigo


def _old_map_residue_code_for_references_DEPRECATED(residue_codigo: str) -> str:
    """
    OLD mapping function for deprecated cp2b_panorama.db database.

    DEPRECATED - DO NOT USE. Kept for reference only.

    The webapp uses hierarchical codes (SECTOR_CULTURE_RESIDUE) but the
    references database uses simpler codes (RESIDUE only).

    This mapping bridges the two naming conventions.

    Args:
        residue_codigo: Webapp code (e.g., 'CANA_VINHACA')

    Returns:
        str: Database code (e.g., 'VINHACA')

    Examples:
        >>> _map_residue_code_for_references('CANA_VINHACA')
        'VINHACA'
        >>> _map_residue_code_for_references('SUINO_DEJETO')
        'DEJETOS_SUINO'
        >>> _map_residue_code_for_references('UNKNOWN_CODE')
        'UNKNOWN_CODE'  # Pass through if no mapping
    """
    code_mapping = {
        # ============================================================================
        # CANA-DE-AÇÚCAR (Top parameters in database)
        # ============================================================================
        'CANA_VINHACA': 'VINHACA',           # 1,007 parameters
        'CANA_BAGACO': 'BAGACO',             # 396 parameters
        'CANA_TORTA_FILTRO': 'TORTA_FILTRO',
        'CANA_PALHA': 'PALHA_CANA',

        # ============================================================================
        # PECUÁRIA - SUÍNOS (Top in database)
        # ============================================================================
        'SUINO_DEJETO': 'DEJETOS_SUINO',     # 1,246 parameters
        'SUINO_DEJETOS': 'DEJETOS_SUINO',

        # ============================================================================
        # PECUÁRIA - BOVINOS
        # ============================================================================
        'BOVINO_DEJETO': 'DEJETOS_BOVINO',
        'BOVINO_DEJETOS': 'DEJETOS_BOVINO',
        'BOVINO_ESTERCO': 'DEJETOS_BOVINO',

        # ============================================================================
        # PECUÁRIA - AVES
        # ============================================================================
        'AVES_CAMA': 'CAMA_AVIARIO',         # 805 parameters
        'AVES_DEJETO': 'DEJETOS_AVES',
        'AVES_DEJETOS': 'DEJETOS_AVES',
        'FRANGO_CAMA': 'CAMA_AVIARIO',

        # ============================================================================
        # CAFÉ
        # ============================================================================
        'CAFE_CASCA': 'CASCA_CAFE',          # 982 parameters
        'CAFE_CASCAS': 'CASCA_CAFE',
        'CAFE_POLPA': 'POLPA_CAFE',

        # ============================================================================
        # CITROS
        # ============================================================================
        'CITROS_BAGACO': 'BAGACO_CITROS',    # 246 parameters
        'CITROS_CASCAS': 'CASCAS_CITROS',
        'CITROS_POLPA': 'POLPA_CITROS',

        # ============================================================================
        # EUCALIPTO
        # ============================================================================
        'EUCALIPTO_CASCA': 'CASCA_EUCALIPTO', # 335 parameters
        'EUCALIPTO_CASCAS': 'CASCA_EUCALIPTO',

        # ============================================================================
        # INDUSTRIAL - FRIGORÍFICO
        # ============================================================================
        'FRIGORIF_VISCERAS': 'VISCERAS',     # 953 parameters
        'FRIGORIF_SANGUE': 'SANGUE',
        'FRIGORIF_REJEITOS': 'REJEITOS',     # 608 parameters
        'ABATE_VISCERAS': 'VISCERAS',
        'ABATE_SANGUE': 'SANGUE',

        # ============================================================================
        # INDUSTRIAL - CERVEJARIA
        # ============================================================================
        'CERVEJA_MALTE': 'BAGACO_MALTE',
        'CERVEJA_LEVEDO': 'LEVEDO_CERVEJA',
        'CERVEJA_BAGACO': 'BAGACO_MALTE',
        'LEVEDO_CERVEJA': 'LEVEDO_CERVEJA',

        # ============================================================================
        # URBANO
        # ============================================================================
        'LODO_ETE': 'LODO_SECUNDARIO',       # 875 parameters
        'ETE_LODO': 'LODO_SECUNDARIO',
        'RSU': 'RSU',
        'RPO': 'RPO',
        'RESIDUO_SOLIDO_URBANO': 'RSU',

        # ============================================================================
        # MILHO
        # ============================================================================
        'MILHO_PALHA': 'PALHA_MILHO',
        'MILHO_SABUGO': 'SABUGO_MILHO',
        'MILHO_BAGACO': 'BAGACO_MILHO',
        'MILHO_SILAGEM': 'SILAGEM_MILHO',

        # ============================================================================
        # SOJA
        # ============================================================================
        'SOJA_PALHA': 'PALHA_SOJA',
        'SOJA_CASCA': 'CASCA_SOJA',
    }

    # Return mapped code or original if no mapping exists
    return code_mapping.get(residue_codigo, residue_codigo)


def _load_scientific_references_dict() -> list:
    """
    INTERNAL: Load references as serializable dicts.

    NOTE: NOT cached to avoid Streamlit serialization issues.
    Database queries are fast enough (<100ms for 674 papers).

    Returns:
        list: List of reference dicts
    """
    from src.services.reference_service import load_all_references

    conn = get_panorama_connection()
    refs = load_all_references(conn)
    return [_scientific_reference_to_dict(ref) for ref in refs]


def load_scientific_references():
    """
    PUBLIC API: Load all scientific references from panorama database.

    Uses cached dict loading internally, then converts to dataclasses.

    Returns:
        List[ScientificReference]: All 674 papers with metadata
    """
    # Load cached dicts
    ref_dicts = _load_scientific_references_dict()
    # Convert to dataclasses
    return [_dict_to_scientific_reference(d) for d in ref_dicts]


def _load_references_for_residue_dict(residue_codigo: str) -> list:
    """
    INTERNAL: Load references as serializable dicts.

    NOTE: NOT cached to avoid Streamlit serialization issues.

    Args:
        residue_codigo: Residue code

    Returns:
        list: List of reference dicts
    """
    from src.services.reference_service import load_references_by_residue

    conn = get_panorama_connection()
    refs = load_references_by_residue(conn, residue_codigo)
    return [_scientific_reference_to_dict(ref) for ref in refs]


def load_references_for_residue(residue_codigo: str):
    """
    PUBLIC API: Load scientific references for a specific residue.

    Automatically maps webapp codes to database codes (e.g., CAFE_CASCA → CASCA_CAFE).

    Args:
        residue_codigo: Residue code from webapp (e.g., 'CAFE_CASCA')

    Returns:
        List[ScientificReference]: Papers linked to this residue
    """
    # MAP webapp code to database code
    db_code = _map_residue_code_for_references(residue_codigo)

    # Load cached dicts with MAPPED code
    ref_dicts = _load_references_for_residue_dict(db_code)

    # Convert to dataclasses
    return [_dict_to_scientific_reference(d) for d in ref_dicts]


# ============================================================================
# DATACLASS CONVERSION HELPERS (FOR STREAMLIT CACHE SERIALIZATION)
# Streamlit @st.cache_data cannot serialize frozen dataclasses.
# Solution: Cache dicts, convert to dataclasses after retrieval.
# ============================================================================

def _scientific_reference_to_dict(ref) -> dict:
    """Convert ScientificReference dataclass to serializable dict."""
    return ref.to_dict()


def _dict_to_scientific_reference(data: dict):
    """Convert serializable dict back to ScientificReference dataclass."""
    from src.models.reference_models import ScientificReference
    from datetime import datetime

    return ScientificReference(
        id=data['id'],
        paper_id=data.get('paper_id'),
        codename=data['codename'],
        codename_short=data.get('codename_short'),
        pdf_filename=data['pdf_filename'],
        pdf_path=data['pdf_path'],
        original_filename=data.get('original_filename'),
        sector=data.get('sector'),
        sector_full=data.get('sector_full'),
        primary_residue=data.get('primary_residue'),
        query_folder=data.get('query_folder'),
        authors=data.get('authors'),
        publication_year=data.get('publication_year'),
        journal=data.get('journal'),
        volume=data.get('volume'),
        issue=data.get('issue'),
        pages=data.get('pages'),
        doi=data.get('doi'),
        title=data.get('title'),
        abstract=data.get('abstract'),
        keywords=data.get('keywords'),
        scopus_id=data.get('scopus_id'),
        pubmed_id=data.get('pubmed_id'),
        google_scholar_link=data.get('google_scholar_link'),
        data_quality=data.get('data_quality', 'Validated'),
        extraction_complete=data.get('extraction_complete', True),
        metadata_complete=data.get('metadata_complete', False),
        verified_by=data.get('verified_by'),
        created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
        last_updated=datetime.fromisoformat(data['last_updated']) if data.get('last_updated') else None,
        notes=data.get('notes')
    )


def _parameter_source_to_dict(source) -> dict:
    """Convert ParameterSource dataclass to serializable dict."""
    # Since ParameterSource is now flattened, just use its to_dict() method
    return source.to_dict()


def _dict_to_parameter_source(data: dict):
    """Convert serializable dict back to ParameterSource dataclass with FLATTENED fields."""
    from src.models.reference_models import ParameterSource

    # Create ParameterSource with flattened reference fields
    return ParameterSource(
        parameter_name=data['parameter_name'],
        parameter_category=data.get('parameter_category'),
        value_min=data.get('value_min'),
        value_mean=data.get('value_mean'),
        value_max=data.get('value_max'),
        unit=data['unit'],
        n_samples=data.get('n_samples'),
        std_deviation=data.get('std_deviation'),
        # FLATTENED reference fields (no nested object)
        reference_id=data['reference_id'],
        reference_codename=data['reference_codename'],
        reference_citation_short=data['reference_citation_short'],
        reference_title=data.get('reference_title'),
        reference_authors=data.get('reference_authors'),
        reference_publication_year=data.get('reference_publication_year'),
        reference_doi=data.get('reference_doi'),
        reference_pdf_path=data['reference_pdf_path'],
        reference_sector_full=data.get('reference_sector_full'),
        reference_data_quality=data['reference_data_quality'],
        reference_metadata_complete=data['reference_metadata_complete'],
        page_number=data.get('page_number'),
        data_quality=data['data_quality'],
        extraction_method=data.get('extraction_method'),
        confidence_score=data.get('confidence_score'),
        measurement_conditions=data.get('measurement_conditions'),
        substrate_type=data.get('substrate_type')
    )


def _load_parameter_sources_dict(residue_codigo: str, parameter_name: str) -> list:
    """
    INTERNAL: Load parameter sources as serializable dicts.

    NOTE: NOT cached to avoid Streamlit serialization issues.
    Database queries are fast enough (typically 5-20 sources per parameter).

    Args:
        residue_codigo: Residue code
        parameter_name: Parameter name

    Returns:
        list: List of dicts
    """
    from src.services.parameter_service import load_parameter_sources

    conn = get_panorama_connection()
    sources = load_parameter_sources(conn, residue_codigo, parameter_name)

    # Convert dataclasses to dicts
    return [_parameter_source_to_dict(s) for s in sources]


def load_parameter_sources_for_residue(residue_codigo: str, parameter_name: str) -> list:
    """
    PUBLIC API: Load validated parameter sources from precision database.

    MIGRATION NOTE: Uses PrecisionDatabaseAdapter to convert validated data
    from CP2B_Precision_Biogas.db to ParameterSource objects expected by Page 2.

    Every parameter measurement includes:
    - Value range (min, mean, max) with unit
    - Source paper (authors, year, title, DOI)
    - Page number where value was found
    - Validation status and context
    - All fields required by Page 2 UI

    Args:
        residue_codigo: Webapp code (e.g., 'CANA_VINHACA', 'VINHACA', 'SUINO_DEJETO')
        parameter_name: Parameter name (e.g., 'COD', 'pH', 'BMP', 'TS', 'VS')

    Returns:
        List[ParameterSource]: List of ParameterSource objects with full traceability.
                               Returns empty list if no validated data found.

    Examples:
        >>> sources = load_parameter_sources_for_residue('CANA_VINHACA', 'COD')
        >>> len(sources)
        16  # 16 validated COD measurements for vinasse
        >>> sources[0].value_mean
        121000.0
        >>> sources[0].reference_citation_short
        'España-Gamboa et al. (2012)'
    """
    try:
        from src.adapters.precision_db_adapter import PrecisionDatabaseAdapter
        from src.models.reference_models import ParameterSource

        # Load sources from precision database
        sources = PrecisionDatabaseAdapter.load_parameter_sources(residue_codigo, parameter_name)

        # Type safety check (prevents caching issues)
        if sources and not isinstance(sources[0], ParameterSource):
            st.error(f"⚠️ Erro interno: tipo de dados incorreto. Por favor, limpe o cache (tecla 'C').")
            return []

        return sources

    except Exception as e:
        st.error(f"Erro ao carregar fontes de {parameter_name} para {residue_codigo}: {str(e)}")
        return []


def _get_all_parameters_dict(residue_codigo: str) -> dict:
    """
    INTERNAL: Load all parameters as nested dict structure.

    NOTE: NOT cached to avoid Streamlit serialization issues.

    Args:
        residue_codigo: Residue code

    Returns:
        dict: Dict[str, List[Dict]] - parameter name → list of source dicts
    """
    from src.services.parameter_service import load_parameters_by_residue

    conn = get_panorama_connection()
    params = load_parameters_by_residue(conn, residue_codigo)

    # Convert nested structure: Dict[str, List[ParameterSource]] → Dict[str, List[Dict]]
    return {
        param_name: [_parameter_source_to_dict(s) for s in sources]
        for param_name, sources in params.items()
    }


def get_all_parameters_for_residue(residue_codigo: str):
    """
    PUBLIC API: Get all parameters for a residue, grouped by parameter name.

    Automatically maps webapp codes to database codes (e.g., SUINO_DEJETO → DEJETOS_SUINO).

    Args:
        residue_codigo: Residue code from webapp (e.g., 'SUINO_DEJETO')

    Returns:
        Dict[str, List[ParameterSource]]: Parameter name → list of sources
    """
    # MAP webapp code to database code
    db_code = _map_residue_code_for_references(residue_codigo)

    # Load cached dict structure with MAPPED code
    params_dict = _get_all_parameters_dict(db_code)

    # Convert back to dataclasses
    return {
        param_name: [_dict_to_parameter_source(d) for d in source_dicts]
        for param_name, source_dicts in params_dict.items()
    }


@st.cache_data(ttl=3600)
def get_parameter_stats_for_residue(residue_codigo: str):
    """
    Get statistical summary of all parameters for a residue.

    Useful for parameter overview tables in UI.

    Args:
        residue_codigo: Residue code

    Returns:
        Dict[str, Dict]: Parameter statistics including paper_count, min/mean/max values
    """
    from src.services.parameter_service import load_parameter_statistics

    conn = get_panorama_connection()
    return load_parameter_statistics(conn, residue_codigo)


def clear_panorama_caches():
    """
    Clear all caches related to panorama database.

    Use this when the panorama database has been updated.
    """
    load_scientific_references.clear()
    load_references_for_residue.clear()
    load_parameter_sources_for_residue.clear()
    get_all_parameters_for_residue.clear()
    get_parameter_stats_for_residue.clear()

