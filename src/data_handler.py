"""
Data Handler Module - Single Responsibility Principle
Handles all data access and processing operations for the biogas dashboard.
"""

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path


def get_db_connection():
    """
    Returns SQLAlchemy engine using database path from Streamlit secrets.
    
    Returns:
        sqlalchemy.engine.Engine: Database connection engine
    """
    db_path = st.secrets["database"]["path"]
    # Convert to absolute path if relative
    if not Path(db_path).is_absolute():
        db_path = Path(__file__).parent.parent / db_path
    
    engine = create_engine(f"sqlite:///{db_path}")
    return engine


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

