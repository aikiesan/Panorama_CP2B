"""
FASE 1: Validacao Completa do Banco de Dados CP2B
==================================================
Script de validacao abrangente antes da integracao
"""

import sqlite3
import pandas as pd
import sys
import io
from pathlib import Path
from datetime import datetime

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

db_path = Path("data/cp2b_panorama.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Results tracker
validation_results = {
    'total_checks': 0,
    'passed': 0,
    'warnings': 0,
    'errors': 0,
    'issues': []
}

def check(name, condition, severity='error', message=''):
    """Helper function to track validation checks"""
    global validation_results
    validation_results['total_checks'] += 1
    
    if condition:
        validation_results['passed'] += 1
        print(f"  [OK] {name}")
        return True
    else:
        if severity == 'error':
            validation_results['errors'] += 1
            print(f"  [ERRO] {name}")
        else:
            validation_results['warnings'] += 1
            print(f"  [AVISO] {name}")
        
        if message:
            print(f"         {message}")
        validation_results['issues'].append({'check': name, 'severity': severity, 'message': message})
        return False

print("=" * 100)
print("FASE 1: VALIDACAO COMPLETA DO BANCO DE DADOS CP2B")
print("=" * 100)
print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# ============================================================================
# 1. VALIDACAO DE ESTRUTURA
# ============================================================================
print("[1] VALIDACAO DE ESTRUTURA DO BANCO")
print("-" * 100)

# Check 1.1: Tabelas essenciais existem
required_tables = ['residuos', 'parametros_quimicos', 'fatores_disponibilidade', 'referencias']
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
existing_tables = [row['name'] for row in cursor.fetchall()]

for table in required_tables:
    check(f"Tabela '{table}' existe", table in existing_tables)

# Check 1.2: Tabelas têm dados
for table in required_tables:
    if table in existing_tables:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
        count = cursor.fetchone()['count']
        check(f"Tabela '{table}' tem dados", count > 0, message=f"Registros: {count}")

print()

# ============================================================================
# 2. VALIDACAO DE VALORES BMP
# ============================================================================
print("[2] VALIDACAO DE VALORES BMP")
print("-" * 100)

# Check 2.1: Todos os resíduos têm BMP
cursor.execute("""
    SELECT COUNT(*) as count
    FROM residuos r
    LEFT JOIN parametros_quimicos p ON r.id = p.residuo_id
    WHERE p.bmp_medio IS NULL
""")
missing_bmp = cursor.fetchone()['count']
check("Todos os residuos tem BMP definido", missing_bmp == 0, 'warning',
      f"{missing_bmp} residuos sem BMP" if missing_bmp > 0 else "")

# Check 2.2: Valores BMP < 1.0 (corrigidos para m3/kg)
cursor.execute("""
    SELECT COUNT(*) as count
    FROM parametros_quimicos
    WHERE bmp_medio >= 1.0
""")
bmp_high = cursor.fetchone()['count']
check("Todos os BMP < 1.0 m3/kg MS", bmp_high == 0, 'error',
      f"{bmp_high} residuos com BMP >= 1.0 (unidade incorreta?)" if bmp_high > 0 else "")

# Check 2.3: Valores BMP > 0
cursor.execute("""
    SELECT COUNT(*) as count
    FROM parametros_quimicos
    WHERE bmp_medio <= 0
""")
bmp_zero = cursor.fetchone()['count']
check("Nenhum BMP <= 0", bmp_zero == 0, 'warning',
      f"{bmp_zero} residuos com BMP <= 0 (falta dados?)" if bmp_zero > 0 else "")

# Check 2.4: BMP ranges válidos (min <= medio <= max)
cursor.execute("""
    SELECT COUNT(*) as count
    FROM parametros_quimicos
    WHERE bmp_min > bmp_medio OR bmp_medio > bmp_max
""")
invalid_ranges = cursor.fetchone()['count']
check("BMP ranges validos (min <= medio <= max)", invalid_ranges == 0, 'error',
      f"{invalid_ranges} residuos com ranges invalidos" if invalid_ranges > 0 else "")

# Check 2.5: Unidade padronizada
cursor.execute("""
    SELECT DISTINCT bmp_unidade, COUNT(*) as count
    FROM parametros_quimicos
    WHERE bmp_unidade IS NOT NULL
    GROUP BY bmp_unidade
""")
unidades = cursor.fetchall()
check("Unidade BMP padronizada", len(unidades) == 1, 'warning',
      f"Encontradas {len(unidades)} unidades diferentes" if len(unidades) > 1 else "")

if len(unidades) > 0:
    for u in unidades:
        print(f"         Unidade: '{u['bmp_unidade']}' ({u['count']} residuos)")

print()

# ============================================================================
# 3. VALIDACAO DE INTEGRIDADE REFERENCIAL
# ============================================================================
print("[3] VALIDACAO DE INTEGRIDADE REFERENCIAL")
print("-" * 100)

# Check 3.1: Todos os resíduos têm parâmetros químicos
cursor.execute("""
    SELECT COUNT(*) as count
    FROM residuos r
    LEFT JOIN parametros_quimicos p ON r.id = p.residuo_id
    WHERE p.id IS NULL
""")
missing_params = cursor.fetchone()['count']
check("Todos os residuos tem parametros quimicos", missing_params == 0, 'warning',
      f"{missing_params} residuos sem parametros" if missing_params > 0 else "")

# Check 3.2: Todos os resíduos têm fatores de disponibilidade
cursor.execute("""
    SELECT COUNT(*) as count
    FROM residuos r
    LEFT JOIN fatores_disponibilidade f ON r.id = f.residuo_id
    WHERE f.id IS NULL
""")
missing_factors = cursor.fetchone()['count']
check("Todos os residuos tem fatores de disponibilidade", missing_factors == 0, 'warning',
      f"{missing_factors} residuos sem fatores" if missing_factors > 0 else "")

# Check 3.3: Parâmetros órfãos (sem resíduo)
cursor.execute("""
    SELECT COUNT(*) as count
    FROM parametros_quimicos p
    LEFT JOIN residuos r ON p.residuo_id = r.id
    WHERE r.id IS NULL
""")
orphan_params = cursor.fetchone()['count']
check("Nenhum parametro orfao", orphan_params == 0, 'warning',
      f"{orphan_params} parametros sem residuo" if orphan_params > 0 else "")

print()

# ============================================================================
# 4. VALIDACAO DE QUALIDADE DE DADOS
# ============================================================================
print("[4] VALIDACAO DE QUALIDADE DE DADOS")
print("-" * 100)

# Check 4.1: Nomes não nulos
cursor.execute("SELECT COUNT(*) as count FROM residuos WHERE nome IS NULL OR nome = ''")
null_names = cursor.fetchone()['count']
check("Todos os residuos tem nome", null_names == 0, 'error',
      f"{null_names} residuos sem nome" if null_names > 0 else "")

# Check 4.2: Setor definido
cursor.execute("SELECT COUNT(*) as count FROM residuos WHERE setor IS NULL OR setor = ''")
null_sector = cursor.fetchone()['count']
check("Todos os residuos tem setor", null_sector == 0, 'warning',
      f"{null_sector} residuos sem setor" if null_sector > 0 else "")

# Check 4.3: Códigos únicos
cursor.execute("""
    SELECT codigo, COUNT(*) as count
    FROM residuos
    WHERE codigo IS NOT NULL
    GROUP BY codigo
    HAVING COUNT(*) > 1
""")
duplicate_codes = cursor.fetchall()
check("Codigos unicos", len(duplicate_codes) == 0, 'error',
      f"{len(duplicate_codes)} codigos duplicados" if len(duplicate_codes) > 0 else "")

# Check 4.4: Distribuição por setor razoável
cursor.execute("""
    SELECT setor, COUNT(*) as count
    FROM residuos
    GROUP BY setor
""")
sector_dist = cursor.fetchall()
print(f"  [INFO] Distribuicao por setor:")
for s in sector_dist:
    setor = s['setor'] if s['setor'] else 'Nao definido'
    print(f"         {setor:<20}: {s['count']:>3} residuos")

print()

# ============================================================================
# 5. VALIDACAO DE REFERENCIAS
# ============================================================================
print("[5] VALIDACAO DE REFERENCIAS CIENTIFICAS")
print("-" * 100)

# Check 5.1: Referências existem
cursor.execute("SELECT COUNT(*) as count FROM referencias")
ref_count = cursor.fetchone()['count']
check("Referencias cientificas cadastradas", ref_count > 0, 'warning',
      f"Total: {ref_count} referencias")

# Check 5.2: Resíduos com referências
cursor.execute("""
    SELECT COUNT(DISTINCT residuo_id) as count
    FROM referencias
    WHERE residuo_id IS NOT NULL
""")
residuos_with_refs = cursor.fetchone()['count']

cursor.execute("SELECT COUNT(*) as count FROM residuos")
total_residuos = cursor.fetchone()['count']

coverage = (residuos_with_refs / total_residuos * 100) if total_residuos > 0 else 0
check("Cobertura de referencias adequada", coverage >= 70, 'warning',
      f"{residuos_with_refs}/{total_residuos} residuos ({coverage:.1f}%)")

print()

# ============================================================================
# 6. EXPORTAR DADOS VALIDADOS
# ============================================================================
print("[6] EXPORTACAO DE DADOS VALIDADOS")
print("-" * 100)

# Export 1: Resumo completo
cursor.execute("""
    SELECT 
        r.id, r.codigo, r.nome, r.setor, r.categoria_nome,
        p.bmp_medio, p.bmp_min, p.bmp_max, p.bmp_unidade,
        p.ts_medio, p.vs_medio, p.cn_medio,
        f.fc_medio, f.fcp_medio, f.fs_medio, f.fl_medio,
        f.disponibilidade_final_media,
        COUNT(ref.id) as num_referencias
    FROM residuos r
    LEFT JOIN parametros_quimicos p ON r.id = p.residuo_id
    LEFT JOIN fatores_disponibilidade f ON r.id = f.residuo_id
    LEFT JOIN referencias ref ON r.id = ref.residuo_id
    GROUP BY r.id
    ORDER BY r.setor, r.nome
""")

df_completo = pd.DataFrame([dict(row) for row in cursor.fetchall()])
output_completo = f"data/validated/residuos_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
Path("data/validated").mkdir(exist_ok=True)
df_completo.to_csv(output_completo, index=False, encoding='utf-8-sig')
print(f"  [OK] Exportado: {output_completo}")
print(f"         {len(df_completo)} residuos exportados")

# Export 2: Apenas BMP para validação
df_bmp = df_completo[['codigo', 'nome', 'setor', 'bmp_medio', 'bmp_min', 'bmp_max', 'bmp_unidade']]
output_bmp = f"data/validated/bmp_validado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df_bmp.to_csv(output_bmp, index=False, encoding='utf-8-sig')
print(f"  [OK] Exportado: {output_bmp}")

# Export 3: Estatísticas
stats = {
    'total_residuos': len(df_completo),
    'bmp_min_geral': df_completo['bmp_medio'].min(),
    'bmp_max_geral': df_completo['bmp_medio'].max(),
    'bmp_medio_geral': df_completo['bmp_medio'].mean(),
    'residuos_com_referencias': int(residuos_with_refs),
    'total_referencias': int(ref_count),
    'setores': df_completo['setor'].nunique()
}

output_stats = f"data/validated/estatisticas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
import json
with open(output_stats, 'w', encoding='utf-8') as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)
print(f"  [OK] Exportado: {output_stats}")

print()

# ============================================================================
# 7. RESUMO FINAL
# ============================================================================
print("=" * 100)
print("RESUMO DA VALIDACAO")
print("=" * 100)

print(f"\nTotal de verificacoes: {validation_results['total_checks']}")
print(f"  [OK] Passou: {validation_results['passed']}")
print(f"  [AVISO] Avisos: {validation_results['warnings']}")
print(f"  [ERRO] Erros: {validation_results['errors']}")

if validation_results['errors'] == 0:
    print("\n" + "="*100)
    print("[SUCESSO] BANCO DE DADOS VALIDADO E PRONTO PARA INTEGRACAO!")
    print("="*100)
else:
    print("\n" + "="*100)
    print("[ATENCAO] CORRIGIR ERROS ANTES DA INTEGRACAO")
    print("="*100)
    print("\nErros encontrados:")
    for issue in validation_results['issues']:
        if issue['severity'] == 'error':
            print(f"  - {issue['check']}: {issue['message']}")

# Save validation report
report = {
    'timestamp': datetime.now().isoformat(),
    'database': str(db_path),
    'results': validation_results,
    'statistics': stats
}

output_report = f"data/validated/validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_report, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print(f"\nRelatorio completo salvo: {output_report}")

conn.close()

print("\n" + "="*100)
print("FASE 1 CONCLUIDA - PROSSEGUIR PARA FASE 2 (Data Loaders)")
print("="*100)

