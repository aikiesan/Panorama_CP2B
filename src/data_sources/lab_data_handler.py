"""
Laboratory Data Handler
Handles chemical and physical parameters for waste characterization and biogas production.
Quick reference data for laboratory parameters.
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
def load_dados_laboratoriais() -> pd.DataFrame:
    """
    Load laboratory reference data for waste characterization.

    Returns:
        pd.DataFrame: Laboratory parameters by waste type
            Columns: tipo_residuo, parametro, valor, unidade, metodo,
                     referencia, observacoes
    """
    engine = get_db_connection()

    try:
        query = "SELECT * FROM dados_laboratoriais"
        df = pd.read_sql(query, engine)

        return df
    except Exception as e:
        st.warning(f"Tabela dados_laboratoriais não encontrada: {e}")
        # Return default reference data if table doesn't exist
        return get_default_lab_data()


def get_default_lab_data() -> pd.DataFrame:
    """
    Provide default laboratory reference data for common waste types.

    Returns:
        pd.DataFrame: Default laboratory parameters
    """
    data = {
        'tipo_residuo': [
            'Esterco Bovino', 'Esterco Bovino', 'Esterco Bovino', 'Esterco Bovino',
            'Esterco Suíno', 'Esterco Suíno', 'Esterco Suíno', 'Esterco Suíno',
            'Cama de Frango', 'Cama de Frango', 'Cama de Frango', 'Cama de Frango',
            'Bagaço de Cana', 'Bagaço de Cana', 'Bagaço de Cana', 'Bagaço de Cana',
            'Vinhaça', 'Vinhaça', 'Vinhaça', 'Vinhaça',
            'RSU (Orgânico)', 'RSU (Orgânico)', 'RSU (Orgânico)', 'RSU (Orgânico)',
            'Palha de Soja', 'Palha de Soja', 'Palha de Soja',
            'Dejeto Piscicultura', 'Dejeto Piscicultura', 'Dejeto Piscicultura'
        ],
        'parametro': [
            'Teor de Sólidos Totais (ST)', 'Teor de Sólidos Voláteis (SV)', 'Relação C/N', 'Potencial Metanogênico (BMP)',
            'Teor de Sólidos Totais (ST)', 'Teor de Sólidos Voláteis (SV)', 'Relação C/N', 'Potencial Metanogênico (BMP)',
            'Teor de Sólidos Totais (ST)', 'Teor de Sólidos Voláteis (SV)', 'Relação C/N', 'Potencial Metanogênico (BMP)',
            'Teor de Sólidos Totais (ST)', 'Teor de Sólidos Voláteis (SV)', 'Relação C/N', 'Potencial Metanogênico (BMP)',
            'Teor de Sólidos Totais (ST)', 'pH', 'DQO', 'Potencial Metanogênico (BMP)',
            'Teor de Sólidos Totais (ST)', 'Teor de Sólidos Voláteis (SV)', 'Relação C/N', 'Potencial Metanogênico (BMP)',
            'Teor de Sólidos Totais (ST)', 'Teor de Sólidos Voláteis (SV)', 'Relação C/N',
            'Teor de Sólidos Totais (ST)', 'Teor de Sólidos Voláteis (SV)', 'Potencial Metanogênico (BMP)'
        ],
        'valor_tipico': [
            '10-15', '70-80', '15-20', '200-300',
            '5-10', '75-85', '10-15', '300-450',
            '60-75', '70-80', '8-12', '250-400',
            '45-55', '95-98', '50-150', '150-250',
            '2-4', '3.5-4.5', '20-40', '200-350',
            '20-30', '70-80', '15-25', '200-400',
            '85-92', '80-90', '20-40',
            '3-8', '60-80', '150-250'
        ],
        'unidade': [
            '%', '% ST', 'adimensional', 'mL CH₄/g SV',
            '%', '% ST', 'adimensional', 'mL CH₄/g SV',
            '%', '% ST', 'adimensional', 'mL CH₄/g SV',
            '%', '% ST', 'adimensional', 'mL CH₄/g SV',
            '%', 'adimensional', 'g O₂/L', 'mL CH₄/g SV',
            '%', '% ST', 'adimensional', 'mL CH₄/g SV',
            '%', '% ST', 'adimensional',
            '%', '% ST', 'mL CH₄/g SV'
        ],
        'metodo': [
            'APHA 2540 B', 'APHA 2540 E', 'Elementar', 'BMP Test',
            'APHA 2540 B', 'APHA 2540 E', 'Elementar', 'BMP Test',
            'APHA 2540 B', 'APHA 2540 E', 'Elementar', 'BMP Test',
            'APHA 2540 B', 'APHA 2540 E', 'Elementar', 'BMP Test',
            'APHA 2540 B', 'APHA 4500-H⁺', 'APHA 5220 D', 'BMP Test',
            'APHA 2540 B', 'APHA 2540 E', 'Elementar', 'BMP Test',
            'APHA 2540 B', 'APHA 2540 E', 'Elementar',
            'APHA 2540 B', 'APHA 2540 E', 'BMP Test'
        ],
        'referencia': [
            'Literatura científica', 'Literatura científica', 'Literatura científica', 'VDI 4630',
            'Literatura científica', 'Literatura científica', 'Literatura científica', 'VDI 4630',
            'Literatura científica', 'Literatura científica', 'Literatura científica', 'VDI 4630',
            'Embrapa/Literatura', 'Embrapa/Literatura', 'Embrapa/Literatura', 'VDI 4630',
            'Setor Sucroalcooleiro', 'Setor Sucroalcooleiro', 'Setor Sucroalcooleiro', 'VDI 4630',
            'ABRELPE/Literatura', 'ABRELPE/Literatura', 'ABRELPE/Literatura', 'VDI 4630',
            'Literatura científica', 'Literatura científica', 'Literatura científica',
            'Literatura científica', 'Literatura científica', 'VDI 4630'
        ]
    }

    return pd.DataFrame(data)


@st.cache_data(ttl=3600)
def get_tipos_residuo_disponiveis() -> list:
    """
    Get list of waste types with laboratory data.

    Returns:
        list: List of waste type names
    """
    df = load_dados_laboratoriais()
    if df.empty or 'tipo_residuo' not in df.columns:
        return []

    return sorted(df['tipo_residuo'].unique().tolist())


@st.cache_data(ttl=3600)
def get_parametros_by_residuo(tipo_residuo: str) -> pd.DataFrame:
    """
    Get all laboratory parameters for a specific waste type.

    Args:
        tipo_residuo: Waste type name

    Returns:
        pd.DataFrame: Laboratory parameters for the waste type
    """
    df = load_dados_laboratoriais()
    if df.empty or 'tipo_residuo' not in df.columns:
        return pd.DataFrame()

    return df[df['tipo_residuo'] == tipo_residuo].copy()


@st.cache_data(ttl=3600)
def get_parametro_especifico(parametro: str) -> pd.DataFrame:
    """
    Get values of a specific parameter across all waste types.

    Args:
        parametro: Parameter name (e.g., 'pH', 'Teor de Sólidos Totais')

    Returns:
        pd.DataFrame: Parameter values for all waste types
    """
    df = load_dados_laboratoriais()
    if df.empty or 'parametro' not in df.columns:
        return pd.DataFrame()

    return df[df['parametro'] == parametro].copy()


@st.cache_data(ttl=3600)
def get_parametros_disponiveis() -> list:
    """
    Get list of available laboratory parameters.

    Returns:
        list: List of parameter names
    """
    df = load_dados_laboratoriais()
    if df.empty or 'parametro' not in df.columns:
        return []

    return sorted(df['parametro'].unique().tolist())


@st.cache_data(ttl=3600)
def buscar_parametro(termo_busca: str) -> pd.DataFrame:
    """
    Search for parameters or waste types containing the search term.

    Args:
        termo_busca: Search term

    Returns:
        pd.DataFrame: Matching laboratory data
    """
    df = load_dados_laboratoriais()
    if df.empty:
        return pd.DataFrame()

    # Case-insensitive search in tipo_residuo and parametro columns
    mask = (
        df['tipo_residuo'].str.contains(termo_busca, case=False, na=False) |
        df['parametro'].str.contains(termo_busca, case=False, na=False)
    )

    return df[mask].copy()


@st.cache_data(ttl=3600)
def get_metodos_analiticos() -> pd.DataFrame:
    """
    Get summary of analytical methods used.

    Returns:
        pd.DataFrame: Analytical methods and their usage count
    """
    df = load_dados_laboratoriais()
    if df.empty or 'metodo' not in df.columns:
        return pd.DataFrame()

    df_metodos = df.groupby('metodo').size().reset_index(name='count')
    return df_metodos.sort_values('count', ascending=False)
