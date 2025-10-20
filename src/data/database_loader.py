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
        
        # Query principal - nova estrutura com tudo na tabela residuos
        query = """
            SELECT 
                id, codigo, nome, setor, categoria_codigo,
                bmp_medio, bmp_min, bmp_max,
                ts_medio, ts_min, ts_max,
                vs_medio, vs_min, vs_max,
                fc_medio, fc_min, fc_max,
                fcp_medio, fcp_min, fcp_max,
                fs_medio, fs_min, fs_max,
                fl_medio, fl_min, fl_max,
                fator_realista, fator_pessimista, fator_otimista
            FROM residuos
            ORDER BY setor, nome
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
                bmp_unit="m³ CH₄/kg MS",
                ts=row['ts_medio'] or 0.0,
                vs=row['vs_medio'] or 0.0,
                vs_basis="% of TS",
                moisture=100 - (row['ts_medio'] or 0.0) if row['ts_medio'] else 0.0,
                cn_ratio=0.0,  # Not in new structure
                nitrogen=None,
                carbon=None,
                ch4_content=0.0,  # Not in new structure
                phosphorus=None,
                potassium=None,
                protein=None,
                toc=None,
                # Ranges
                bmp_range=ParameterRange(
                    min=row['bmp_min'] or 0.0,
                    mean=row['bmp_medio'] or 0.0,
                    max=row['bmp_max'] or 0.0,
                    unit="m³ CH₄/kg MS"
                ) if row['bmp_min'] and row['bmp_max'] else None
            )
            
            # Availability Factors - Calculate final_availability using correct formula
            fc = row['fc_medio'] or 0.95
            fcp = row['fcp_medio'] or 0.05
            fs = row['fs_medio'] or 1.0
            fl = row['fl_medio'] or 1.0
            
            # CORRECT FORMULA: FC × (1 - FCp) × FS × FL × 100
            final_availability = fc * (1 - fcp) * fs * fl * 100
            
            availability = AvailabilityFactors(
                fc=fc,
                fcp=fcp,
                fs=fs,
                fl=fl,
                final_availability=final_availability,
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
            
            # Carregar municípios
            municipalities = self._load_top_municipalities(row['codigo'], row['setor'], limit=20)
            
            # Criar ResidueData
            residue = ResidueData(
                name=row['nome'],
                category=row['categoria_codigo'] or row['setor'],
                icon="📊",  # Default icon
                generation=f"Setor: {row['setor']}",
                destination="Biodigestão anaeróbia",
                chemical_params=chemical,
                availability=availability,
                operational=operational,
                scenarios={
                    "Pessimista": 0.0,  # Será calculado
                    "Realista": 0.0,
                    "Otimista": 0.0,
                    "Teórico (100%)": 0.0
                },
                top_municipalities=municipalities,
                justification=f"Resíduo do setor {row['setor']}",
                references=references
            )
            
            # Adicionar setor como atributo dinâmico
            residue.setor = row['setor']
            residue.codigo = row['codigo']
            
            # Calcular cenários usando municípios
            residue.scenarios = self._calculate_scenarios(residue)
            
            return residue
            
        except Exception as e:
            print(f"Erro ao criar resíduo {row['nome']}: {e}")
            return None
    
    def _load_references(self, residuo_id: int) -> List[ScientificReference]:
        """Carrega referências científicas para um resíduo"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Verificar se a tabela referencias existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='referencias'
        """)
        
        if not cursor.fetchone():
            # Tabela não existe, retornar lista vazia
            conn.close()
            return []
        
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
    
    def _load_top_municipalities(self, residuo_codigo: str, setor: str, limit: int = 20) -> List[Dict]:
        """Carrega top N municípios para um resíduo específico baseado no setor"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Mapear setor para coluna da tabela municipios
        sector_column_map = {
            'AG_AGRICULTURA': 'ch4_rea_agricultura',
            'PC_PECUARIA': 'ch4_rea_pecuaria',
            'UR_URBANO': 'ch4_rea_urbano',
            'IN_INDUSTRIAL': 'ch4_rea_total'  # fallback
        }
        
        col = sector_column_map.get(setor, 'ch4_rea_total')
        
        # Query top municípios
        query = f"""
            SELECT 
                codigo_municipio as code,
                nome_municipio as name,
                {col} as production_nm3,
                ({col} * 10 / 1000) as energy_mwh
            FROM municipios
            WHERE {col} > 0
            ORDER BY {col} DESC
            LIMIT ?
        """
        
        cursor.execute(query, (limit,))
        municipalities = []
        for row in cursor.fetchall():
            municipalities.append({
                'code': row[0],
                'name': row[1],
                'production_nm3': row[2],
                'energy_mwh': row[3]
            })
        
        conn.close()
        return municipalities
    
    def _calculate_scenarios(self, residue_data: ResidueData) -> Dict[str, float]:
        """Calculate CH4 potential for all scenarios using sector totals and residue factors"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get total CH4 potential for the sector
        setor = getattr(residue_data, 'setor', 'AG_AGRICULTURA')
        sector_column_map = {
            'AG_AGRICULTURA': 'ch4_rea_agricultura',
            'PC_PECUARIA': 'ch4_rea_pecuaria', 
            'UR_URBANO': 'ch4_rea_urbano',
            'IN_INDUSTRIAL': 'ch4_rea_total'
        }
        
        col = sector_column_map.get(setor, 'ch4_rea_total')
        
        cursor.execute(f"SELECT SUM({col}) as total FROM municipios")
        total_sector_ch4 = cursor.fetchone()[0] or 0
        
        conn.close()
        
        if total_sector_ch4 == 0:
            return {
                "Pessimista": 0.0,
                "Realista": 0.0,
                "Otimista": 0.0,
                "Teórico (100%)": 0.0
            }
        
        # Get factors from database (fator_realista, fator_pessimista, fator_otimista)
        # These are already calculated in the database
        codigo = getattr(residue_data, 'codigo', '')
        
        # Get factors from database
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT fator_pessimista, fator_realista, fator_otimista 
            FROM residuos 
            WHERE codigo = ?
        """, (codigo,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0] is not None:
            # Use factors from database
            avail_pess = row[0]  # fator_pessimista
            avail_real = row[1]  # fator_realista  
            avail_opt = row[2]   # fator_otimista
        else:
            # Fallback to calculated factors
            avail = residue_data.availability
            avail_pess = avail.fc * 0.8 * (1 - avail.fcp * 1.2) * avail.fs * 0.8 * avail.fl * 0.8
            avail_real = avail.fc * (1 - avail.fcp) * avail.fs * avail.fl
            avail_opt = avail.fc * 1.2 * (1 - avail.fcp * 0.8) * avail.fs * 1.0 * avail.fl * 1.2
        
        # Theoretical: 100%
        avail_theo = 1.0
        
        return {
            "Pessimista": total_sector_ch4 * avail_pess / 1_000_000,  # Million m³
            "Realista": total_sector_ch4 * avail_real / 1_000_000,
            "Otimista": total_sector_ch4 * avail_opt / 1_000_000,
            "Teórico (100%)": total_sector_ch4 * avail_theo / 1_000_000
        }


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

