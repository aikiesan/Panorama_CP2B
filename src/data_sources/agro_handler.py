"""
Defesa Agropecuária SP Data Handler
Handles official agricultural and livestock data from São Paulo State.
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
def load_residuos_pecuarios() -> pd.DataFrame:
    """
    Load livestock residues data.

    Returns:
        pd.DataFrame: Livestock residues by municipality
            Columns: codigo_municipio, tipo_criacao, num_cabecas,
                     residuo_ton_dia, potencial_biogas_m3_ano
    """
    engine = get_db_connection()

    try:
        query = "SELECT * FROM residuos_pecuarios"
        df = pd.read_sql(query, engine)

        # Ensure proper data types
        numeric_cols = ['num_cabecas', 'residuo_ton_dia', 'potencial_biogas_m3_ano']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        return df
    except Exception as e:
        st.warning(f"Tabela residuos_pecuarios não encontrada: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def get_tipos_criacao_disponiveis() -> list:
    """
    Get list of available livestock types.

    Returns:
        list: List of livestock type names
    """
    df = load_residuos_pecuarios()
    if df.empty or 'tipo_criacao' not in df.columns:
        return []

    return sorted(df['tipo_criacao'].unique().tolist())


@st.cache_data(ttl=3600)
def get_rebanho_by_tipo(tipo_criacao: str) -> pd.DataFrame:
    """
    Get livestock data for a specific type.

    Args:
        tipo_criacao: Type of livestock (e.g., 'Bovinos', 'Suínos')

    Returns:
        pd.DataFrame: Livestock data filtered by type
    """
    df = load_residuos_pecuarios()
    if df.empty or 'tipo_criacao' not in df.columns:
        return pd.DataFrame()

    return df[df['tipo_criacao'] == tipo_criacao].copy()


@st.cache_data(ttl=3600)
def get_top_criadores(tipo_criacao: str, n: int = 10) -> pd.DataFrame:
    """
    Get top N municipalities by livestock head count.

    Args:
        tipo_criacao: Type of livestock
        n: Number of top municipalities

    Returns:
        pd.DataFrame: Top livestock producers
    """
    df = get_rebanho_by_tipo(tipo_criacao)
    if df.empty or 'num_cabecas' not in df.columns:
        return pd.DataFrame()

    df_top = df.nlargest(n, 'num_cabecas')
    return df_top


@st.cache_data(ttl=3600)
def get_total_residuos_pecuarios() -> dict:
    """
    Calculate total livestock residues across all types.

    Returns:
        dict: Summary statistics
            - total_cabecas
            - total_residuos_ton_dia
            - total_potencial_biogas_m3_ano
            - tipos_criacao_count
    """
    df = load_residuos_pecuarios()
    if df.empty:
        return {
            'total_cabecas': 0,
            'total_residuos_ton_dia': 0,
            'total_potencial_biogas_m3_ano': 0,
            'tipos_criacao_count': 0
        }

    return {
        'total_cabecas': df['num_cabecas'].sum() if 'num_cabecas' in df.columns else 0,
        'total_residuos_ton_dia': df['residuo_ton_dia'].sum() if 'residuo_ton_dia' in df.columns else 0,
        'total_potencial_biogas_m3_ano': df['potencial_biogas_m3_ano'].sum() if 'potencial_biogas_m3_ano' in df.columns else 0,
        'tipos_criacao_count': len(df['tipo_criacao'].unique()) if 'tipo_criacao' in df.columns else 0
    }


@st.cache_data(ttl=3600)
def get_defesa_agropecuaria_stats() -> dict:
    """
    Get official statistics from Defesa Agropecuária SP.

    Returns:
        dict: Official agricultural statistics
            - propriedades_cadastradas
            - area_inspecionada_ha
            - estabelecimentos_certificados
    """
    engine = get_db_connection()

    try:
        query = "SELECT * FROM defesa_agropecuaria"
        df = pd.read_sql(query, engine)

        if df.empty:
            return {}

        # Aggregate stats
        stats = {
            'propriedades_cadastradas': df['propriedades_cadastradas'].sum() if 'propriedades_cadastradas' in df.columns else 0,
            'area_inspecionada_ha': df['area_inspecionada_ha'].sum() if 'area_inspecionada_ha' in df.columns else 0,
            'estabelecimentos_certificados': df['estabelecimentos_certificados'].sum() if 'estabelecimentos_certificados' in df.columns else 0
        }

        return stats
    except Exception as e:
        st.warning(f"Tabela defesa_agropecuaria não encontrada: {e}")
        return {}
