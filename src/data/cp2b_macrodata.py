"""
CP2B Macro Data - Agregação e análise municipal do biogás em SP
Dados validados via Google Earth Engine + Jupyter Notebooks
Status: Phase 2 Integration

Fornece dados agregados de:
- 425 plantas de biogás mapeadas
- 184 municípios do estado de SP
- 9 tipos de resíduos com SAF validado
- Fatores validados via geosspatial analysis
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
import sqlite3
from pathlib import Path


# =============================================================================
# MODELOS DE DADOS
# =============================================================================

@dataclass
class MunicipalAggregation:
    """Agregação de dados por município"""
    cd_mun: int
    nm_mun: str
    qtd_plantas: int
    qtd_plantas_cana: int
    qtd_plantas_citros: int
    qtd_plantas_pecuaria: int
    area_total_cana_ha: float
    area_total_citros_ha: float
    area_total_soja_ha: float
    area_total_pastagem_ha: float
    potencial_total_m3_ano: float
    potencial_cana_m3_ano: float
    potencial_citros_m3_ano: float
    potencial_pecuaria_m3_ano: float
    potencial_urbano_m3_ano: float
    residuos_total_ton: float
    rank_estadual: int
    categoria_potencial: str  # MUITO ALTO, ALTO, MÉDIO, BAIXO


@dataclass
class SAFValidated:
    """Fatores de disponibilidade validados via Google Earth Engine"""
    tipo_residuo: str  # cana_palha, cana_bagaco, citros_bagaco, etc
    saf_teorico: float
    fc_coleta: float  # Fator de coleta
    fcp_competicao: float  # Fator de competição
    fs_sazonal: float  # Fator sazonal
    fl_logistico_20km: float  # Fator logístico (raio 20km)
    rpr_value: float  # RPR (Raio Potencial Ótimo)
    bmp_m3_ton_ms: int  # Potencial metanogênico
    fonte_validacao: str  # "Google Earth Engine", "MapBiomas", etc
    saf_real_ajustado: float  # SAF final ajustado


@dataclass
class PlantaWebapp:
    """Dados agregados de uma planta (sem coordenadas geográficas)"""
    id_webapp: int
    cd_mun: int
    nm_mun: str
    name: str
    cultura_dominante: str
    categoria_potencial: str
    potencial_total_m3_ano: float
    potencial_cana_m3_ano: float
    potencial_citros_m3_ano: float
    potencial_pecuaria_m3_ano: float
    residuo_cana_ton: Optional[float] = None
    residuo_milho_ton: Optional[float] = None
    residuo_soja_ton: Optional[float] = None
    residuo_bovino_ton: Optional[float] = None
    bio_cana: Optional[float] = None
    bio_citros: Optional[float] = None
    bio_pecuaria: Optional[float] = None


# =============================================================================
# CARREGADOR DE DADOS DO JUPYTER DB
# =============================================================================

class CP2BDataLoader:
    """
    Carrega dados validados do banco Jupyter

    Localizacao: ~/Documents/CP2B/Validacao_dados/06_Outputs/01_Banco_Dados/cp2b_panorama.db
    """

    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "data" / "cp2b_macrodata_validated.db"

        # Se não existe, usar o Jupyter DB
        if not self.db_path.exists():
            # Usar banco original do Jupyter
            jupyter_path = Path.home() / "Documents" / "CP2B" / "Validacao_dados" / "06_Outputs" / "01_Banco_Dados" / "cp2b_panorama.db"
            if jupyter_path.exists():
                self.db_path = jupyter_path

    def load_municipios(self) -> List[MunicipalAggregation]:
        """Carrega agregação de dados por município"""
        municipios = []

        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM municipios_resumo ORDER BY rank_estadual")

            for row in cursor.fetchall():
                municipios.append(MunicipalAggregation(
                    cd_mun=row[1],
                    nm_mun=row[2],
                    qtd_plantas=row[3],
                    qtd_plantas_cana=row[4] or 0,
                    qtd_plantas_citros=row[5] or 0,
                    qtd_plantas_pecuaria=row[6] or 0,
                    area_total_cana_ha=row[7] or 0.0,
                    area_total_citros_ha=row[8] or 0.0,
                    area_total_soja_ha=row[9] or 0.0,
                    area_total_pastagem_ha=row[10] or 0.0,
                    potencial_total_m3_ano=row[11] or 0.0,
                    potencial_cana_m3_ano=row[12] or 0.0,
                    potencial_citros_m3_ano=row[13] or 0.0,
                    potencial_pecuaria_m3_ano=row[14] or 0.0,
                    potencial_urbano_m3_ano=row[15] or 0.0,
                    residuos_total_ton=row[16] or 0.0,
                    rank_estadual=row[17],
                    categoria_potencial=row[18] or "INDEFINIDO"
                ))

            conn.close()
        except Exception as e:
            print(f"Erro ao carregar municípios: {e}")

        return municipios

    def load_saf_validados(self) -> List[SAFValidated]:
        """Carrega fatores SAF validados via Google Earth Engine"""
        fatores = []

        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM fatores_validados")

            for row in cursor.fetchall():
                fatores.append(SAFValidated(
                    tipo_residuo=row[0],
                    saf_teorico=row[1] or 0.0,
                    fc_coleta=row[2] or 0.0,
                    fcp_competicao=row[3] or 0.0,
                    fs_sazonal=row[4] or 0.0,
                    fl_logistico_20km=row[5] or 0.0,
                    rpr_value=row[6] or 0.0,
                    bmp_m3_ton_ms=row[7] or 0,
                    fonte_validacao=row[8] or "Não especificado",
                    saf_real_ajustado=row[9] or 0.0
                ))

            conn.close()
        except Exception as e:
            print(f"Erro ao carregar SAF: {e}")

        return fatores


# =============================================================================
# DADOS CARREGADOS E CACHE
# =============================================================================

_loader = CP2BDataLoader()

# Cache de dados
_municipios_cache: Optional[List[MunicipalAggregation]] = None
_saf_cache: Optional[List[SAFValidated]] = None


def get_municipios() -> List[MunicipalAggregation]:
    """Retorna lista de 184 municípios com agregação"""
    global _municipios_cache
    if _municipios_cache is None:
        _municipios_cache = _loader.load_municipios()
    return _municipios_cache


def get_saf_validados() -> List[SAFValidated]:
    """Retorna fatores SAF validados (9 tipos de resíduo)"""
    global _saf_cache
    if _saf_cache is None:
        _saf_cache = _loader.load_saf_validados()
    return _saf_cache


def get_municipio_by_code(cd_mun: int) -> Optional[MunicipalAggregation]:
    """Busca município por código IBGE"""
    municipios = get_municipios()
    for m in municipios:
        if m.cd_mun == cd_mun:
            return m
    return None


def get_municipio_by_name(nm_mun: str) -> Optional[MunicipalAggregation]:
    """Busca município por nome"""
    municipios = get_municipios()
    for m in municipios:
        if m.nm_mun.lower() == nm_mun.lower():
            return m
    return None


def get_top_municipios(n: int = 20) -> List[MunicipalAggregation]:
    """Retorna top N municípios por potencial"""
    municipios = get_municipios()
    return sorted(municipios, key=lambda x: x.potencial_total_m3_ano, reverse=True)[:n]


def get_saf_by_residuo(tipo_residuo: str) -> Optional[SAFValidated]:
    """Busca fatores SAF por tipo de resíduo"""
    fatores = get_saf_validados()
    for f in fatores:
        if f.tipo_residuo.lower() == tipo_residuo.lower():
            return f
    return None


def get_estadisticas_estaduais() -> Dict:
    """Retorna estatísticas agregadas do estado de SP"""
    municipios = get_municipios()

    return {
        "total_municipios": len(municipios),
        "total_plantas": sum(m.qtd_plantas for m in municipios),
        "potencial_total_m3_ano": sum(m.potencial_total_m3_ano for m in municipios),
        "potencial_cana_m3_ano": sum(m.potencial_cana_m3_ano for m in municipios),
        "potencial_citros_m3_ano": sum(m.potencial_citros_m3_ano for m in municipios),
        "potencial_pecuaria_m3_ano": sum(m.potencial_pecuaria_m3_ano for m in municipios),
        "potencial_urbano_m3_ano": sum(m.potencial_urbano_m3_ano for m in municipios),
        "area_total_cana_ha": sum(m.area_total_cana_ha for m in municipios),
        "area_total_citros_ha": sum(m.area_total_citros_ha for m in municipios),
        "residuos_total_ton": sum(m.residuos_total_ton for m in municipios),
    }


# =============================================================================
# ESTATÍSTICAS E ANÁLISES
# =============================================================================

def get_distribuicao_por_cultura() -> Dict:
    """Retorna distribuição de potencial por cultura"""
    stats = get_estadisticas_estaduais()
    total = stats["potencial_total_m3_ano"]

    return {
        "Cana": {
            "potencial_m3_ano": stats["potencial_cana_m3_ano"],
            "pct": (stats["potencial_cana_m3_ano"] / total * 100) if total > 0 else 0,
            "area_ha": stats["area_total_cana_ha"]
        },
        "Citros": {
            "potencial_m3_ano": stats["potencial_citros_m3_ano"],
            "pct": (stats["potencial_citros_m3_ano"] / total * 100) if total > 0 else 0,
            "area_ha": stats["area_total_citros_ha"]
        },
        "Pecuária": {
            "potencial_m3_ano": stats["potencial_pecuaria_m3_ano"],
            "pct": (stats["potencial_pecuaria_m3_ano"] / total * 100) if total > 0 else 0,
        },
        "Urbano": {
            "potencial_m3_ano": stats["potencial_urbano_m3_ano"],
            "pct": (stats["potencial_urbano_m3_ano"] / total * 100) if total > 0 else 0,
        }
    }


def get_categorias_potencial() -> Dict:
    """Retorna distribuição por categoria de potencial"""
    municipios = get_municipios()

    categorias = {}
    for municipio in municipios:
        cat = municipio.categoria_potencial
        if cat not in categorias:
            categorias[cat] = {
                "qtd_municipios": 0,
                "qtd_plantas": 0,
                "potencial_m3_ano": 0.0
            }

        categorias[cat]["qtd_municipios"] += 1
        categorias[cat]["qtd_plantas"] += municipio.qtd_plantas
        categorias[cat]["potencial_m3_ano"] += municipio.potencial_total_m3_ano

    return categorias


# =============================================================================
# INIT
# =============================================================================

if __name__ == "__main__":
    # Test
    print("CP2B Macro Data - Testing...")
    print(f"Municípios: {len(get_municipios())}")
    print(f"SAF Validados: {len(get_saf_validados())}")
    print(f"Top 5: {[m.nm_mun for m in get_top_municipios(5)]}")
    print(f"Stats: {get_estadisticas_estaduais()}")
