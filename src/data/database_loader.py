"""
Database Loader - Carrega residuos do banco cp2b_panorama.db
Substitui dados hardcoded por dados atualizados do banco
"""

import sqlite3
import streamlit as st
from pathlib import Path
from typing import Dict, List, Optional
from src.models.residue_models import (
    ResidueData,
    ChemicalParameters,
    AvailabilityFactors,
    OperationalParameters,
    ScientificReference,
    ParameterRange
)


class DatabaseLoader:
    """Carrega dados de resíduos do banco SQL"""
    
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "data" / "cp2b_panorama.db"
        if not self.db_path.exists():
            raise FileNotFoundError(f"Banco de dados não encontrado: {self.db_path}")
    
    def _get_connection(self):
        """Cria conexão com o banco"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    @st.cache_data(ttl=3600)
    def load_all_residues(_self) -> Dict[str, ResidueData]:
        """Carrega todos os resíduos do banco"""
        residues = {}
        conn = _self._get_connection()
        cursor = conn.cursor()
        
        # Query principal - join de todas as tabelas
        query = """
            SELECT 
                r.id, r.codigo, r.nome, r.setor, r.categoria_nome, r.icon,
                r.generation, r.destination, r.justification,
                p.bmp_medio, p.bmp_min, p.bmp_max, p.bmp_unidade,
                p.ts_medio, p.ts_min, p.ts_max,
                p.vs_medio, p.vs_min, p.vs_max,
                p.cn_medio, p.cn_min, p.cn_max,
                p.ch4_medio, p.ch4_min, p.ch4_max,
                f.fc_medio, f.fc_min, f.fc_max,
                f.fcp_medio, f.fcp_min, f.fcp_max,
                f.fs_medio, f.fs_min, f.fs_max,
                f.fl_medio, f.fl_min, f.fl_max,
                f.disponibilidade_final_media
            FROM residuos r
            LEFT JOIN parametros_quimicos p ON r.id = p.residuo_id
            LEFT JOIN fatores_disponibilidade f ON r.id = f.residuo_id
            ORDER BY r.setor, r.nome
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for row in rows:
            residue_data = _self._create_residue_from_row(row)
            if residue_data:
                residues[row['nome']] = residue_data
        
        conn.close()
        return residues
    
    def _create_residue_from_row(self, row) -> Optional[ResidueData]:
        """Cria objeto ResidueData a partir de uma linha do banco"""
        try:
            # Chemical Parameters
            chemical = ChemicalParameters(
                bmp=row['bmp_medio'] or 0.0,
                bmp_unit=row['bmp_unidade'] or "m³ CH₄/kg MS",
                ts=row['ts_medio'] or 0.0,
                vs=row['vs_medio'] or 0.0,
                vs_basis="% of TS",
                moisture=100 - (row['ts_medio'] or 0.0) if row['ts_medio'] else 0.0,
                cn_ratio=row['cn_medio'] or 0.0,
                nitrogen=None,
                carbon=None,
                ch4_content=row['ch4_medio'] or 0.0,
                phosphorus=None,
                potassium=None,
                protein=None,
                toc=None,
                # Ranges
                bmp_range=ParameterRange(
                    min=row['bmp_min'] or 0.0,
                    mean=row['bmp_medio'] or 0.0,
                    max=row['bmp_max'] or 0.0,
                    unit=row['bmp_unidade'] or "m³ CH₄/kg MS"
                ) if row['bmp_min'] and row['bmp_max'] else None,
                cn_ratio_range=ParameterRange(
                    min=row['cn_min'] or 0.0,
                    mean=row['cn_medio'] or 0.0,
                    max=row['cn_max'] or 0.0,
                    unit=""
                ) if row['cn_min'] and row['cn_max'] else None
            )
            
            # Availability Factors
            availability = AvailabilityFactors(
                fc=row['fc_medio'] or 0.0,
                fcp=row['fcp_medio'] or 0.0,
                fs=row['fs_medio'] or 1.0,
                fl=row['fl_medio'] or 1.0,
                final_availability=row['disponibilidade_final_media'] or 0.0,
                # Ranges
                fc_range=ParameterRange(
                    min=row['fc_min'] or 0.0,
                    mean=row['fc_medio'] or 0.0,
                    max=row['fc_max'] or 0.0,
                    unit=""
                ) if row['fc_min'] and row['fc_max'] else None,
                fcp_range=ParameterRange(
                    min=row['fcp_min'] or 0.0,
                    mean=row['fcp_medio'] or 0.0,
                    max=row['fcp_max'] or 0.0,
                    unit=""
                ) if row['fcp_min'] and row['fcp_max'] else None,
                fs_range=ParameterRange(
                    min=row['fs_min'] or 0.0,
                    mean=row['fs_medio'] or 0.0,
                    max=row['fs_max'] or 0.0,
                    unit=""
                ) if row['fs_min'] and row['fs_max'] else None,
                fl_range=ParameterRange(
                    min=row['fl_min'] or 0.0,
                    mean=row['fl_medio'] or 0.0,
                    max=row['fl_max'] or 0.0,
                    unit=""
                ) if row['fl_min'] and row['fl_max'] else None
            )
            
            # Operational Parameters (valores padrão)
            operational = OperationalParameters(
                hrt="30-45 dias",
                temperature="35-40°C (mesofílica)",
                fi_ratio=None,
                olr="2-4 kg DQO/m³/dia",
                reactor_type="CSTR",
                tan_threshold="<2000 mg/L",
                vfa_limit="<2000 mg/L",
                hrt_range=ParameterRange(min=30.0, mean=37.5, max=45.0, unit="dias"),
                temperature_range=ParameterRange(min=35.0, mean=37.5, max=40.0, unit="°C")
            )
            
            # Carregar referencias
            references = self._load_references(row['id'])
            
            # Criar ResidueData
            residue = ResidueData(
                name=row['nome'],
                category=row['categoria_nome'] or row['setor'],
                icon=row['icon'] or "📊",
                generation=row['generation'] or f"Setor: {row['setor']}",
                destination=row['destination'] or "Biodigestão anaeróbia",
                chemical_params=chemical,
                availability=availability,
                operational=operational,
                scenarios={
                    "Pessimista": 0.0,  # Será calculado
                    "Realista": 0.0,
                    "Otimista": 0.0,
                    "Teórico (100%)": 0.0
                },
                top_municipalities=[],  # Pode ser carregado se necessário
                justification=row['justification'] or f"Resíduo do setor {row['setor']}",
                references=references
            )
            
            return residue
            
        except Exception as e:
            print(f"Erro ao criar resíduo {row['nome']}: {e}")
            return None
    
    def _load_references(self, residuo_id: int) -> List[ScientificReference]:
        """Carrega referências científicas para um resíduo"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT parametro, resumo, referencias_completas, doi, ano
            FROM referencias
            WHERE residuo_id = ?
            ORDER BY ano DESC
        """, (residuo_id,))
        
        references = []
        for row in cursor.fetchall():
            ref = ScientificReference(
                title=row['resumo'] or f"Referência {row['parametro']}",
                authors="",  # Não disponível nesta tabela
                year=row['ano'] or 2020,
                doi=row['doi'] or "",
                scopus_link="",  # Não disponível nesta tabela
                journal="",  # Não disponível nesta tabela
                relevance=row['parametro'] or "",
                key_findings=[row['referencias_completas']] if row['referencias_completas'] else [],
                data_type=row['parametro'] or "BMP"
            )
            references.append(ref)
        
        conn.close()
        return references


# Singleton instance
_loader = None

def get_database_loader() -> DatabaseLoader:
    """Retorna instância única do loader"""
    global _loader
    if _loader is None:
        _loader = DatabaseLoader()
    return _loader


@st.cache_data(ttl=3600)
def load_all_residues_from_db() -> Dict[str, ResidueData]:
    """Função de conveniência para carregar todos os resíduos"""
    loader = get_database_loader()
    return loader.load_all_residues()

