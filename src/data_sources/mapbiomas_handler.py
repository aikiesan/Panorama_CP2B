"""
MapBiomas Data Handler
Handles land use and land cover data from MapBiomas.
"""

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path


def get_db_connection():
    """Get database connection."""
    db_path = st.secrets["database"]["path"]
    if not Path(db_path).is_absolute():
        db_path = Path(__file__).parent.parent.parent / db_path
    engine = create_engine(f"sqlite:///{db_path}")
    return engine


@st.cache_data(ttl=3600)
def load_uso_solo() -> pd.DataFrame:
    """
    Load land use/land cover data from MapBiomas.

    Returns:
        pd.DataFrame: Land use data by municipality
            Columns: codigo_municipio, ano, classe_uso, area_km2, percentual_territorio
    """
    engine = get_db_connection()

    try:
        query = "SELECT * FROM uso_solo_mapbiomas"
        df = pd.read_sql(query, engine)

        # Ensure proper data types
        numeric_cols = ['area_km2', 'percentual_territorio']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        return df
    except Exception as e:
        st.warning(f"Tabela uso_solo_mapbiomas não encontrada: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def get_classes_uso_disponíveis() -> list:
    """
    Get list of available land use classes.

    Returns:
        list: List of land use class names
    """
    df = load_uso_solo()
    if df.empty or 'classe_uso' not in df.columns:
        return []

    return sorted(df['classe_uso'].unique().tolist())


@st.cache_data(ttl=3600)
def get_uso_solo_municipio(codigo_municipio: int) -> pd.DataFrame:
    """
    Get land use data for a specific municipality.

    Args:
        codigo_municipio: IBGE municipality code

    Returns:
        pd.DataFrame: Land use distribution for the municipality
    """
    df = load_uso_solo()
    if df.empty or 'codigo_municipio' not in df.columns:
        return pd.DataFrame()

    return df[df['codigo_municipio'] == codigo_municipio].copy()


@st.cache_data(ttl=3600)
def get_area_total_por_classe() -> pd.DataFrame:
    """
    Calculate total area by land use class across all municipalities.

    Returns:
        pd.DataFrame: Aggregated area by land use class
            Columns: classe_uso, area_total_km2, percentual_estado
    """
    df = load_uso_solo()
    if df.empty:
        return pd.DataFrame()

    if 'classe_uso' not in df.columns or 'area_km2' not in df.columns:
        return pd.DataFrame()

    df_agg = df.groupby('classe_uso')['area_km2'].sum().reset_index()
    df_agg.columns = ['classe_uso', 'area_total_km2']

    # Calculate percentage of state
    total_area = df_agg['area_total_km2'].sum()
    df_agg['percentual_estado'] = (df_agg['area_total_km2'] / total_area * 100) if total_area > 0 else 0

    return df_agg.sort_values('area_total_km2', ascending=False)


@st.cache_data(ttl=3600)
def get_municipios_by_uso_dominante(classe_uso: str) -> pd.DataFrame:
    """
    Get municipalities where a specific land use class is dominant.

    Args:
        classe_uso: Land use class name

    Returns:
        pd.DataFrame: Municipalities with specified dominant land use
    """
    df = load_uso_solo()
    if df.empty:
        return pd.DataFrame()

    # Find dominant land use for each municipality
    df_max = df.loc[df.groupby('codigo_municipio')['area_km2'].idxmax()]

    # Filter by specified class
    return df_max[df_max['classe_uso'] == classe_uso].copy()
