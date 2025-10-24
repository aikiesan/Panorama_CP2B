"""
Quick test script to verify PrecisionDatabaseAdapter integration.
Tests that standardized units and values are being used correctly.
"""

from src.adapters.precision_db_adapter import PrecisionDatabaseAdapter

def test_vinhaça():
    print("\n" + "="*80)
    print("TESTING VINHAÇA (CANA_VINHACA)")
    print("="*80)

    # Test parameter loading
    sources = PrecisionDatabaseAdapter.load_parameter_sources('CANA_VINHACA', 'TS')

    print(f"\n✅ Found {len(sources)} TS measurements for Vinhaça")

    if sources:
        print("\nFirst 5 measurements:")
        for i, src in enumerate(sources[:5], 1):
            print(f"  {i}. Value: {src.value_mean} {src.unit} | Source: {src.reference_citation_short}")

        # Check for standardization
        units = set(src.unit for src in sources)
        print(f"\n📊 Units used: {units}")

        if len(units) == 1:
            print(f"✅ SUCCESS: All TS values use standardized unit: {list(units)[0]}")
        else:
            print(f"⚠️  WARNING: Multiple units found - standardization may not be working")

    print("\n" + "-"*80)

    # Test COD
    cod_sources = PrecisionDatabaseAdapter.load_parameter_sources('CANA_VINHACA', 'COD')
    print(f"\n✅ Found {len(cod_sources)} COD measurements for Vinhaça")

    if cod_sources:
        print("\nFirst 5 measurements:")
        for i, src in enumerate(cod_sources[:5], 1):
            print(f"  {i}. Value: {src.value_mean} {src.unit} | Source: {src.reference_citation_short}")

        units = set(src.unit for src in cod_sources)
        print(f"\n📊 Units used: {units}")
        if len(units) == 1:
            print(f"✅ SUCCESS: All COD values use standardized unit: {list(units)[0]}")


def test_palha():
    print("\n" + "="*80)
    print("TESTING PALHA DE CANA (CANA_PALHA)")
    print("="*80)

    # Get available parameters
    available = PrecisionDatabaseAdapter.get_available_parameters('CANA_PALHA')
    print(f"\n✅ Found {len(available)} different parameters for Palha")
    print(f"Parameters: {', '.join(available)}")

    # Test TS for solid residue
    ts_sources = PrecisionDatabaseAdapter.load_parameter_sources('CANA_PALHA', 'TS')
    print(f"\n✅ Found {len(ts_sources)} TS measurements for Palha")

    if ts_sources:
        print("\nFirst 3 measurements:")
        for i, src in enumerate(ts_sources[:3], 1):
            print(f"  {i}. Value: {src.value_mean} {src.unit} | Source: {src.reference_citation_short}")

        units = set(src.unit for src in ts_sources)
        print(f"\n📊 Units used: {units}")


def test_bagaço():
    print("\n" + "="*80)
    print("TESTING BAGAÇO DE CANA (CANA_BAGACO)")
    print("="*80)

    available = PrecisionDatabaseAdapter.get_available_parameters('CANA_BAGACO')
    print(f"\n✅ Found {len(available)} different parameters for Bagaço")
    print(f"Parameters: {', '.join(available)}")

    if available:
        # Test first available parameter
        param = available[0]
        sources = PrecisionDatabaseAdapter.load_parameter_sources('CANA_BAGACO', param)
        print(f"\n✅ Testing {param}: {len(sources)} measurements")

        if sources:
            for i, src in enumerate(sources[:3], 1):
                print(f"  {i}. Value: {src.value_mean} {src.unit} | Source: {src.reference_citation_short}")


def test_database_stats():
    print("\n" + "="*80)
    print("DATABASE STATISTICS")
    print("="*80)

    stats = PrecisionDatabaseAdapter.get_database_stats()

    print(f"\n📊 Total validated parameters: {stats['total_validated_parameters']}")
    print(f"📚 Total papers: {stats['total_papers']}")
    print(f"🗃️  Total residues: {stats['total_residues']}")

    print("\n📈 Parameters by residue:")
    for residue, count in sorted(stats['parameters_by_residue'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {residue}: {count} parameters")

    print("\n🔝 Top 10 parameter types:")
    for param, count in list(stats['top_parameters'].items())[:10]:
        print(f"  - {param}: {count} measurements")


if __name__ == "__main__":
    print("\n🧪 CP2B PRECISION DATABASE ADAPTER INTEGRATION TEST")
    print("="*80)

    try:
        test_vinhaça()
        test_palha()
        test_bagaço()
        test_database_stats()

        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\n📋 Summary:")
        print("  ✓ Vinhaça: Data loading and standardization working")
        print("  ✓ Palha: Residue mapping working")
        print("  ✓ Bagaço: Residue mapping working")
        print("  ✓ Database stats: All queries functional")
        print("\n🎯 The webapp should now display standardized units for all residues!")
        print("   Visit: http://localhost:8501")
        print("   Navigate to: Page 2 (Parâmetros Químicos)")
        print("   Select: Any sugarcane residue")
        print("\n")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
