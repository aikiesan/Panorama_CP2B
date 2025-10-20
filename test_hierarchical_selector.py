"""
Página de Teste - Seletor Hierárquico 3 Níveis
Phase 5: Demonstração do novo seletor Setor -> Cultura -> Resíduo
"""

import streamlit as st

# Configure page
st.set_page_config(
    page_title="Teste Hierárquico - PanoramaCP2B",
    page_icon="🧪",
    layout="wide"
)

# Import components
from src.ui.hierarchical_selector import render_full_selector_3_levels
from src.data.residue_registry import get_residue_data

# ==============================================================================
# HEADER
# ==============================================================================

st.markdown("# 🧪 Teste do Seletor Hierárquico (3 Níveis)")
st.markdown("**Phase 5:** Demonstração do novo seletor Setor → Cultura → Resíduo")

st.markdown("---")

# ==============================================================================
# HIERARCHICAL SELECTOR
# ==============================================================================

selected_residue_name = render_full_selector_3_levels(key_prefix="test")

# ==============================================================================
# DISPLAY SELECTED RESIDUE DATA
# ==============================================================================

if selected_residue_name:
    st.markdown("---")
    st.markdown("## ✅ Resíduo Selecionado")

    residue_data = get_residue_data(selected_residue_name)

    if residue_data:
        # Show residue summary in columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="📦 Resíduo",
                value=residue_data.name,
                delta=f"Setor: {residue_data.category}"
            )

        with col2:
            st.metric(
                label="⚡ BMP",
                value=f"{residue_data.chemical_params.bmp:.0f}",
                delta=residue_data.chemical_params.bmp_unit
            )

        with col3:
            st.metric(
                label="📊 Disponibilidade",
                value=f"{residue_data.availability.final_availability:.1f}%",
                delta=f"SAF Real: {residue_data.saf_real or 'N/A'}"
            )

        # Show full data
        st.markdown("### 📋 Dados Completos")

        with st.expander("Ver Parâmetros Químicos"):
            st.json(residue_data.chemical_params.to_dict())

        with st.expander("Ver Fatores de Disponibilidade"):
            st.json(residue_data.availability.to_dict())

        with st.expander("Ver Cenários"):
            st.json(residue_data.scenarios)

        # Show hierarchy information if available
        if residue_data.culture_group:
            st.markdown(f"""
            **Hierarquia Completa:**
            - 🏭 Setor: {residue_data.category}
            - 🌾 Cultura: {residue_data.culture_group}
            - 📦 Resíduo: {residue_data.name}
            """)

    else:
        st.error(f"⚠️ Dados não encontrados para o resíduo '{selected_residue_name}'")

else:
    st.info("👆 Selecione um setor, cultura e resíduo acima para ver os dados")

# ==============================================================================
# FOOTER
# ==============================================================================

st.markdown("---")
st.markdown("""
### 🎯 Instruções para Uso

O novo seletor hierárquico funciona em 3 níveis:

1. **Setor** (ex: Agricultura, Pecuária)
2. **Cultura** (ex: Cana-de-Açúcar, Citros, Café...)
3. **Resíduo** (ex: Vinhaça, Bagaço, Palha...)

**Vantagens:**
- ✅ Organização clara por cultura
- ✅ Navegação intuitiva
- ✅ Dropdown de resíduos mais curto e focado
- ✅ Fácil mudança de nível com botões "Trocar"

**Para usar em suas páginas:**

```python
from src.ui.hierarchical_selector import render_full_selector_3_levels
from src.data.residue_registry import get_residue_data

# Renderizar seletor
selected_residue_name = render_full_selector_3_levels(key_prefix="minha_pagina")

if selected_residue_name:
    residue_data = get_residue_data(selected_residue_name)
    # ... usar dados do resíduo
```
""")
