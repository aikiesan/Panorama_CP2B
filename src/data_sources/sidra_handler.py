"""
SIDRA/IBGE Data Handler
Handles data from SIDRA (Sistema IBGE de Recuperação Automática).
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
def load_sidra_agricola() -> pd.DataFrame:
    """
    Load agricultural production data from SIDRA.

    Returns:
        pd.DataFrame: Agricultural data by municipality
            Columns: codigo_municipio, ano, cultura, area_plantada_ha,
                     producao_ton, valor_producao_mil_reais
    """
    engine = get_db_connection()

    try:
        query = "SELECT * FROM residuos_agricolas"
        df = pd.read_sql(query, engine)

        # Ensure proper data types
        numeric_cols = ['area_plantada_ha', 'producao_ton', 'valor_producao_mil_reais',
                       'residuo_gerado_ton', 'potencial_biogas_m3']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        return df
    except Exception as e:
        st.warning(f"Tabela residuos_agricolas não encontrada: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def get_culturas_disponiveis() -> list:
    """
    Get list of available agricultural crops.

    Returns:
        list: List of crop names
    """
    df = load_sidra_agricola()
    if df.empty:
        return []

    if 'cultura' in df.columns:
        return sorted(df['cultura'].unique().tolist())
    return []


@st.cache_data(ttl=3600)
def get_producao_by_cultura(cultura: str) -> pd.DataFrame:
    """
    Get production data for a specific crop.

    Args:
        cultura: Crop name (e.g., 'Cana-de-açúcar', 'Soja')

    Returns:
        pd.DataFrame: Production data filtered by crop
    """
    df = load_sidra_agricola()
    if df.empty or 'cultura' not in df.columns:
        return pd.DataFrame()

    return df[df['cultura'] == cultura].copy()


@st.cache_data(ttl=3600)
def get_top_produtores(cultura: str, n: int = 10) -> pd.DataFrame:
    """
    Get top N municipalities by production for a given crop.

    Args:
        cultura: Crop name
        n: Number of top municipalities

    Returns:
        pd.DataFrame: Top producers with production metrics
    """
    df = get_producao_by_cultura(cultura)
    if df.empty or 'producao_ton' not in df.columns:
        return pd.DataFrame()

    df_top = df.nlargest(n, 'producao_ton')
    return df_top


@st.cache_data(ttl=3600)
def get_total_residuos_agricola() -> dict:
    """
    Calculate total agricultural residues across all crops.

    Returns:
        dict: Summary statistics
            - total_producao_ton
            - total_residuos_ton
            - total_potencial_biogas_m3
            - culturas_count
    """
    df = load_sidra_agricola()
    if df.empty:
        return {
            'total_producao_ton': 0,
            'total_residuos_ton': 0,
            'total_potencial_biogas_m3': 0,
            'culturas_count': 0
        }

    return {
        'total_producao_ton': df['producao_ton'].sum() if 'producao_ton' in df.columns else 0,
        'total_residuos_ton': df['residuo_gerado_ton'].sum() if 'residuo_gerado_ton' in df.columns else 0,
        'total_potencial_biogas_m3': df['potencial_biogas_m3'].sum() if 'potencial_biogas_m3' in df.columns else 0,
        'culturas_count': len(df['cultura'].unique()) if 'cultura' in df.columns else 0
    }
