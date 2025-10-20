import sys
import io
sys.path.insert(0, '.')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("DIAGNOSTICO CRITICO - VERIFICANDO DADOS COMPLETOS")
print("=" * 70)

from src.data.residue_registry import get_residue_data, RESIDUES_REGISTRY

# Verificar Bagaço de Cana
print("\n1. TESTANDO 'Bagaco de Cana':")
print("-" * 70)

residue = get_residue_data("Bagaco de Cana")
if residue:
    print(f"[OK] Residuo encontrado: {residue.name}")
    print(f"  Category: {residue.category}")
    print(f"  Setor: {getattr(residue, 'setor', 'N/A')}")
    print(f"  Icon: {residue.icon}")
    print(f"  Generation: {residue.generation}")
    
    # Chemical params
    if residue.chemical_params:
        cp = residue.chemical_params
        print(f"\n  Chemical Parameters:")
        print(f"    BMP: {cp.bmp}")
        print(f"    VS: {cp.vs}")
    else:
        print("\n  [ERRO] Chemical params = None!")
    
    # Availability
    if residue.availability:
        av = residue.availability
        print(f"\n  Availability:")
        print(f"    FC: {av.fc}")
        print(f"    FCP: {av.fcp}")
        print(f"    FS: {av.fs}")
        print(f"    FL: {av.fl}")
        print(f"    Final: {av.final_availability}")
    else:
        print("\n  [ERRO] Availability = None!")
    
    # Scenarios
    print(f"\n  Scenarios: {residue.scenarios}")
    
    # Top municipalities
    print(f"\n  Top municipalities: {len(residue.top_municipalities)} municipios")
    if residue.top_municipalities:
        print(f"    Primeiro: {residue.top_municipalities[0]}")
else:
    print("[ERRO] Residuo nao encontrado!")

# Verificar outro resíduo
print("\n\n2. TESTANDO 'Esterco bovino':")
print("-" * 70)

residue2 = get_residue_data("Esterco bovino")
if residue2:
    print(f"[OK] Residuo encontrado: {residue2.name}")
    print(f"  BMP: {residue2.chemical_params.bmp if residue2.chemical_params else 'N/A'}")
    print(f"  FS: {residue2.availability.fs if residue2.availability else 'N/A'}")
    print(f"  Scenarios: {residue2.scenarios}")
    print(f"  Top municipalities: {len(residue2.top_municipalities)} municipios")
else:
    print("[ERRO] Residuo nao encontrado!")

# Verificar total de municípios em todos os resíduos
print("\n\n3. VERIFICANDO TOP_MUNICIPALITIES EM TODOS OS RESIDUOS:")
print("-" * 70)

total_with_municipalities = 0
total_without_municipalities = 0

for name, residue in RESIDUES_REGISTRY.items():
    if residue.top_municipalities and len(residue.top_municipalities) > 0:
        total_with_municipalities += 1
    else:
        total_without_municipalities += 1

print(f"Com municipios: {total_with_municipalities}")
print(f"Sem municipios: {total_without_municipalities}")

if total_without_municipalities > 0:
    print(f"\n[ALERTA] {total_without_municipalities} residuos SEM municipios!")
    print("Primeiros 5 sem municipios:")
    count = 0
    for name, residue in RESIDUES_REGISTRY.items():
        if not residue.top_municipalities or len(residue.top_municipalities) == 0:
            print(f"  - {name}")
            count += 1
            if count >= 5:
                break

# Testar cálculo de cenários
print("\n\n4. VERIFICANDO CALCULOS DE CENARIOS:")
print("-" * 70)

from src.models.calculations import calculate_ch4_potential

# Pegar um resíduo com dados
test_residue = get_residue_data("Bagaco de Cana")
if test_residue and test_residue.top_municipalities:
    mun = test_residue.top_municipalities[0]
    print(f"Testando calculo para: {test_residue.name}")
    print(f"  Municipio: {mun['name']}")
    print(f"  Production: {mun['production_ton']}")
    print(f"  BMP: {test_residue.chemical_params.bmp if test_residue.chemical_params else 'N/A'}")
    
    # Calcular potencial
    try:
        potential = calculate_ch4_potential(
            production_ton=mun['production_ton'],
            bmp=test_residue.chemical_params.bmp,
            availability_factor=test_residue.availability.final_availability
        )
        print(f"  Potencial calculado: {potential:.2f} m3 CH4")
    except Exception as e:
        print(f"  [ERRO] Calculo falhou: {e}")
else:
    print("[ERRO] Nao foi possivel testar calculo (sem municipios)")

print("\n" + "=" * 70)
print("FIM DO DIAGNOSTICO")
print("=" * 70)

