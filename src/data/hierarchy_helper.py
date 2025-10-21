"""
Hierarchy Helper Functions for CP2B Database
Created: 2025-10-21
Purpose: Provides hierarchical filtering for residues
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple

class HierarchyHelper:
    """Helper class for hierarchical residue filtering"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            self.db_path = Path(__file__).parent.parent.parent / "data" / "cp2b_panorama.db"
        else:
            self.db_path = Path(db_path)
    
    def get_setores(self) -> List[Tuple[str, str, str]]:
        """
        Get list of all sectors
        Returns: [(codigo, nome, emoji), ...]
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT setor_codigo, setor_nome, setor_emoji
            FROM subsetor_hierarchy
            ORDER BY ordem_setor
        """)
        
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_subsetores(self, setor_codigo: str = None) -> List[Tuple[str, str]]:
        """
        Get subsetores for a given setor
        Args:
            setor_codigo: Filter by sector (optional)
        Returns: [(codigo, nome), ...]
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        if setor_codigo:
            cursor.execute("""
                SELECT subsetor_codigo, subsetor_nome
                FROM subsetor_hierarchy
                WHERE setor_codigo = ?
                ORDER BY ordem_subsetor
            """, (setor_codigo,))
        else:
            cursor.execute("""
                SELECT subsetor_codigo, subsetor_nome
                FROM subsetor_hierarchy
                ORDER BY ordem_setor, ordem_subsetor
            """)
        
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_residuos_by_subsetor(self, subsetor_codigo: str) -> List[Dict]:
        """
        Get all residues in a subsetor with their data
        Args:
            subsetor_codigo: Subsetor code
        Returns: List of residue dicts
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                codigo, nome, setor, subsetor_codigo, subsetor_nome,
                fator_realista, fator_pessimista, fator_otimista,
                fc_medio, fcp_medio, fs_medio, fl_medio,
                bmp_medio, ts_medio, vs_medio
            FROM residuos
            WHERE subsetor_codigo = ?
            ORDER BY fator_realista DESC
        """, (subsetor_codigo,))
        
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result
    
    def get_hierarchy_tree(self) -> Dict:
        """
        Get complete hierarchy as nested dict
        Returns: {
            'AG_AGRICULTURA': {
                'nome': 'Agricultura',
                'emoji': '🌾',
                'subsetores': {
                    'CANA': {
                        'nome': 'Cana-de-açúcar',
                        'residuos': [...]
                    }
                }
            }
        }
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all hierarchy data
        cursor.execute("""
            SELECT 
                h.setor_codigo, h.setor_nome, h.setor_emoji,
                h.subsetor_codigo, h.subsetor_nome,
                r.codigo as residuo_codigo, r.nome as residuo_nome,
                r.fator_realista
            FROM subsetor_hierarchy h
            LEFT JOIN residuos r ON r.subsetor_codigo = h.subsetor_codigo
            ORDER BY h.ordem_setor, h.ordem_subsetor, r.fator_realista DESC
        """)
        
        tree = {}
        for row in cursor.fetchall():
            setor_cod = row['setor_codigo']
            subsetor_cod = row['subsetor_codigo']
            
            # Initialize setor if needed
            if setor_cod not in tree:
                tree[setor_cod] = {
                    'nome': row['setor_nome'],
                    'emoji': row['setor_emoji'],
                    'subsetores': {}
                }
            
            # Initialize subsetor if needed
            if subsetor_cod not in tree[setor_cod]['subsetores']:
                tree[setor_cod]['subsetores'][subsetor_cod] = {
                    'nome': row['subsetor_nome'],
                    'residuos': []
                }
            
            # Add residue if exists
            if row['residuo_codigo']:
                tree[setor_cod]['subsetores'][subsetor_cod]['residuos'].append({
                    'codigo': row['residuo_codigo'],
                    'nome': row['residuo_nome'],
                    'saf': row['fator_realista'] * 100
                })
        
        conn.close()
        return tree
    
    def get_residuos_filtered(self, setor: str = None, subsetor: str = None) -> List[Dict]:
        """
        Get residues with optional filtering
        Args:
            setor: Setor code (optional)
            subsetor: Subsetor code (optional)
        Returns: List of residue dicts
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT 
                codigo, nome, setor, subsetor_codigo, subsetor_nome,
                fator_realista, fc_medio, fcp_medio, fs_medio, fl_medio
            FROM residuos
            WHERE 1=1
        """
        params = []
        
        if setor:
            query += " AND setor = ?"
            params.append(setor)
        
        if subsetor:
            query += " AND subsetor_codigo = ?"
            params.append(subsetor)
        
        query += " ORDER BY fator_realista DESC"
        
        cursor.execute(query, params)
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result


# Example usage
if __name__ == "__main__":
    helper = HierarchyHelper()
    
    # Get hierarchy tree
    tree = helper.get_hierarchy_tree()
    
    # Print structure
    for setor_cod, setor_data in tree.items():
        print(f"\n{setor_data['emoji']} {setor_data['nome']}")
        for subsetor_cod, subsetor_data in setor_data['subsetores'].items():
            print(f"  └─ {subsetor_data['nome']} ({len(subsetor_data['residuos'])} resíduos)")
            for residuo in subsetor_data['residuos'][:2]:  # Show first 2
                print(f"      ├─ {residuo['nome']} (SAF: {residuo['saf']:.2f}%)")
