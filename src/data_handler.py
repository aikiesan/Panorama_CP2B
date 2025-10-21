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
        "residues": "webapp/panorama_cp2b_final.db"
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
        pd.DataFrame: Availability factors (SAF)
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
def calculate_saf(fc: float, fcp: float, fs: float, fl: float) -> float:
    """
    Calculate SAF (Sistema de Aproveitamento de Fatores).

    Formula: SAF = FC × FCp × FS × FL × 100%

    IMPORTANT: FCp represents % AVAILABLE after competition (NOT % competing).
    - FCp = 0.70 means 70% available (30% goes to competing uses)
    - FCp = 0.20 means 20% available (80% goes to competing uses like cogeração)

    Args:
        fc: Collection factor (0-1) - Technical collection efficiency
        fcp: Competition factor (0-1) - % AVAILABLE after competing uses
        fs: Seasonality factor (0-1) - Seasonal availability
        fl: Logistic factor (0-1) - Logistic/transport viability

    Returns:
        float: SAF percentage (0-100)

    Examples:
        Bagaço cana (high competition - cogeração):
        - FC=0.95, FCp=0.20 (20% available, 80% to cogeração), FS=0.90, FL=0.90
        - SAF = 0.95 × 0.20 × 0.90 × 0.90 × 100 = 15.4%

        Dejetos suínos (low competition):
        - FC=0.90, FCp=0.75 (75% available), FS=1.0, FL=0.90
        - SAF = 0.90 × 0.75 × 1.0 × 0.90 × 100 = 60.8%
    """
    return fc * fcp * fs * fl * 100.0

