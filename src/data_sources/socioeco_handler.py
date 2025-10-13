"""
Socioeconomic Data Handler
Handles socioeconomic data from IBGE (PIB, employment, income, etc.).
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
def load_dados_socioeconomicos() -> pd.DataFrame:
    """
    Load socioeconomic data from IBGE.

    Returns:
        pd.DataFrame: Socioeconomic indicators by municipality
            Columns: codigo_municipio, ano, pib_mil_reais, pib_per_capita,
                     populacao, idhm, gini, emprego_formal, renda_media
    """
    engine = get_db_connection()

    try:
        query = "SELECT * FROM dados_socioeconomicos"
        df = pd.read_sql(query, engine)

        # Ensure proper data types
        numeric_cols = ['pib_mil_reais', 'pib_per_capita', 'populacao', 'idhm',
                       'gini', 'emprego_formal', 'renda_media']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        return df
    except Exception as e:
        st.warning(f"Tabela dados_socioeconomicos não encontrada: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def get_pib_municipios(ano: int = None) -> pd.DataFrame:
    """
    Get PIB (GDP) data for municipalities.

    Args:
        ano: Year filter (optional)

    Returns:
        pd.DataFrame: PIB data by municipality
    """
    df = load_dados_socioeconomicos()
    if df.empty:
        return pd.DataFrame()

    if ano and 'ano' in df.columns:
        df = df[df['ano'] == ano]

    if 'pib_mil_reais' in df.columns and 'codigo_municipio' in df.columns:
        return df[['codigo_municipio', 'ano', 'pib_mil_reais', 'pib_per_capita']].copy()

    return pd.DataFrame()


@st.cache_data(ttl=3600)
def get_top_municipios_pib(n: int = 10, ano: int = None) -> pd.DataFrame:
    """
    Get top N municipalities by PIB.

    Args:
        n: Number of top municipalities
        ano: Year filter (optional)

    Returns:
        pd.DataFrame: Top municipalities by PIB
    """
    df = get_pib_municipios(ano)
    if df.empty or 'pib_mil_reais' not in df.columns:
        return pd.DataFrame()

    df_top = df.nlargest(n, 'pib_mil_reais')
    return df_top


@st.cache_data(ttl=3600)
def get_indicadores_sociais(codigo_municipio: int) -> dict:
    """
    Get social indicators for a specific municipality.

    Args:
        codigo_municipio: IBGE municipality code

    Returns:
        dict: Social indicators (IDHM, Gini, etc.)
    """
    df = load_dados_socioeconomicos()
    if df.empty or 'codigo_municipio' not in df.columns:
        return {}

    df_mun = df[df['codigo_municipio'] == codigo_municipio]
    if df_mun.empty:
        return {}

    # Get most recent data
    df_mun = df_mun.sort_values('ano', ascending=False).iloc[0]

    indicators = {}
    if 'idhm' in df_mun.index:
        indicators['idhm'] = df_mun['idhm']
    if 'gini' in df_mun.index:
        indicators['gini'] = df_mun['gini']
    if 'emprego_formal' in df_mun.index:
        indicators['emprego_formal'] = df_mun['emprego_formal']
    if 'renda_media' in df_mun.index:
        indicators['renda_media'] = df_mun['renda_media']

    return indicators


@st.cache_data(ttl=3600)
def get_correlacao_pib_residuos() -> pd.DataFrame:
    """
    Calculate correlation between PIB and waste generation.

    Returns:
        pd.DataFrame: Correlation data for analysis
    """
    from ..data_handler import load_all_municipalities

    df_socio = load_dados_socioeconomicos()
    df_mun = load_all_municipalities()

    if df_socio.empty or df_mun.empty:
        return pd.DataFrame()

    # Merge on municipality code
    if 'codigo_municipio' in df_socio.columns and 'codigo_municipio' in df_mun.columns:
        df_merged = pd.merge(
            df_socio,
            df_mun[['codigo_municipio', 'total_final_m_ano', 'total_urbano_m_ano']],
            on='codigo_municipio',
            how='inner'
        )
        return df_merged

    return pd.DataFrame()
