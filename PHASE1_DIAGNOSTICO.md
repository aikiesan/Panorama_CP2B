# FASE 1 - DIAGNÓSTICO: Integração de Dados CP2B

**Data**: 2025-10-17
**Status**: ✅ Completo
**Próxima Fase**: Phase 2 - Integração

---

## 📊 RESUMO EXECUTIVO

| Aspecto | Banco Atual (PanoramaCP2B) | Banco Validado (Jupyter) | Status |
|---------|---------------------------|-------------------------|--------|
| **Foco** | Resíduos individuais | Plantas agregadas (425) | Complementares ✅ |
| **Tabelas** | 11 | 4 principais | Não há conflito |
| **Dados** | 14 resíduos | 184 municípios | Sem redundância |
| **Escopo** | Disponibilidade | Panorama estadual | Diferentes perspectivas |

---

## 🏗️ ESTRUTURA BANCO ATUAL (PanoramaCP2B/data/cp2b_panorama.db)

### Tabelas Existentes (11)

```
1. residues (7 registros)
   └─ Resíduos individuais: Cana, Citros, Pecuária, etc

2. chemical_params (7)
   └─ Parâmetros: BMP, TS, VS, Umidade

3. operational_params (6)
   └─ TRH, temperatura, reactor_type

4. availability_factors (7)
   └─ FC, FCp, FS, FL, final_availability

5. scenarios (7)
   └─ Pessimista, Realista, Otimista, Teórico

6. scientific_references (50)
   └─ DOI, autores, ano, relevância

7-11. Supporting tables
   └─ decomposition, economics, ghg_emissions, etc
```

**Propósito**: Detalhe técnico de cada resíduo para análise de disponibilidade

---

## 🗺️ ESTRUTURA BANCO VALIDADO (Jupyter Output)

**Localização**: `C:\Users\Lucas\Documents\CP2B\Validacao_dados\06_Outputs\01_Banco_Dados\cp2b_panorama.db`

### Tabelas Principais (4)

#### 1. **plantas_webapp** (425 registros - CRÍTICA)
```
├─ Identificação
│  ├─ id_webapp (PK)
│  ├─ cd_mun, nm_mun (município)
│  └─ name (identificação da planta)
│
├─ Georreferenciamento
│  ├─ latitude, longitude (200 plantas com coordenadas)
│  ├─ buffer_area_km2
│  └─ [NÃO será usado - sem mapas no Streamlit]
│
├─ Culturas e Áreas (ha)
│  ├─ cultura_dominante
│  ├─ area_cana_ha, area_citros_ha, area_soja_ha, area_cafe_ha
│  ├─ pct_cana, pct_citros, pct_soja, etc
│  └─ tipo_dominante, tipo_predominante
│
├─ Potenciais (m³/ano)
│  ├─ potencial_total_m3_ano ⭐ (CHAVE)
│  ├─ potencial_total_m3_dia
│  ├─ potencial_cana_m3_ano
│  ├─ potencial_citros_m3_ano
│  ├─ potencial_pastagem_m3_ano
│  └─ potencial_urbano_m3_ano
│
├─ Resíduos (ton)
│  ├─ residuo_cana_ton
│  ├─ residuo_milho_ton
│  ├─ residuo_soja_ton
│  └─ residuo_bovino_ton
│
├─ Biogás por origem
│  ├─ bio_cana
│  ├─ bio_citros
│  ├─ bio_pecuaria
│  └─ bio_agricola
│
└─ Rankings
   ├─ rank_agricola
   ├─ rank_urbano
   └─ rank_combinado
```

#### 2. **municipios_resumo** (184 registros)
```
├─ Identificação
│  ├─ id_municipio (PK)
│  ├─ cd_mun (IBGE)
│  └─ nm_mun
│
├─ Agregados
│  ├─ qtd_plantas (total)
│  ├─ qtd_plantas_cana
│  ├─ qtd_plantas_citros
│  └─ qtd_plantas_pecuaria
│
├─ Áreas (ha)
│  ├─ area_total_cana_ha
│  ├─ area_total_citros_ha
│  ├─ area_total_soja_ha
│  └─ area_total_pastagem_ha
│
├─ Potenciais (m³/ano) ⭐
│  ├─ potencial_total_m3_ano
│  ├─ potencial_cana_m3_ano
│  ├─ potencial_citros_m3_ano
│  ├─ potencial_pecuaria_m3_ano
│  └─ potencial_urbano_m3_ano
│
├─ Resíduos (ton)
│  └─ residuos_total_ton
│
├─ Ranking
│  ├─ rank_estadual
│  └─ categoria_potencial (MUITO ALTO, ALTO, MÉDIO, BAIXO)
```

#### 3. **fatores_validados** (9 tipos de resíduo)
```
├─ Tipo de resíduo
│  ├─ cana_palha
│  ├─ cana_bagaco
│  ├─ cana_vinhaca
│  ├─ citros_bagaco
│  ├─ pecuaria_bovino
│  ├─ pecuaria_suino
│  ├─ pecuaria_avicultura
│  ├─ urbano_rsu
│  └─ urbano_podas
│
├─ Fatores SAF (validados via Google Earth Engine)
│  ├─ saf_teorico
│  ├─ fc_coleta
│  ├─ fcp_competicao
│  ├─ fs_sazonal
│  ├─ fl_logistico_20km
│  └─ saf_real_ajustado ⭐
│
├─ Potencial
│  ├─ bmp_m3_ton_ms
│  ├─ rpr_value
│  └─ fonte_validacao
```

#### 4. **parametros_tecnicos** (9 tipos)
```
├─ Tipo de resíduo
└─ Parâmetros operacionais
   ├─ producao_unitaria
   ├─ unidade_producao
   ├─ geracao_residuo_kg_ms_dia
   ├─ umidade_pct
   ├─ vs_pct_ts
   ├─ c_n_ratio
   ├─ densidade_kg_m3
   └─ periodo_geracao_dias
```

---

## 🔄 ANÁLISE DE SOBREPOSIÇÃO

### O que FALTA no PanoramaCP2B:
- ❌ Dados municipais agregados (184 municípios)
- ❌ Rankings estaduais
- ❌ Distribuição geográfica (sem mapa, só dados)
- ❌ Análise por região/mesorregião
- ❌ Fatores SAF validados por Google Earth Engine

### O que SOBRA do PanoramaCP2B:
- ✅ Disponibilidade detalhada de resíduos
- ✅ Cenários (Pessimista/Realista/Otimista/Teórico)
- ✅ Parâmetros operacionais técnicos
- ✅ Referências científicas (50+)

### Conclusão:
**NÃO HÁ CONFLITO** - Bancos são complementares!
- PanoramaCP2B = Análise técnica por resíduo
- Jupyter DB = Panorama agregado por município

---

## 📋 CHECKLIST INTEGRAÇÃO

### Dados a integrar AO PanoramaCP2B:

```sql
-- ADICIONAR À tabelas Streamlit:
1. ✅ municipios_resumo (184)
   └─ Criar: src/data/cp2b_macrodata.py

2. ✅ plantas_webapp (425) [SEM coordenadas geográficas]
   └─ Usar apenas: nm_mun, cultura_dominante, potencial_total_m3_ano

3. ✅ fatores_validados (9 tipos)
   └─ Complementar com os já existentes
   └─ Adicionar: saf_real_ajustado (validado)

4. ✅ parametros_tecnicos (9 tipos)
   └─ Comparar com existentes
   └─ Mesclar se não houver conflito
```

---

## 🎯 ESTRATÉGIA DE INTEGRAÇÃO

### Opção A: Dados SEPARADOS (Recomendado)
```python
# src/data/cp2b_macrodata.py
├─ MUNICIPIOS_RESUMO_DATA = {...}  # 184 municípios
├─ PLANTAS_AGREGADAS_DATA = {...}  # 425 plantas (sem coords)
└─ FATORES_SAF_VALIDADOS = {...}   # 9 tipos

# Criará Nova Página 5: "Panorama São Paulo"
# Sem afetar páginas 1-4 existentes
```

### Opção B: Dados INTEGRADOS
```python
# Atualizar existing residues com fatores validados
# RISCO: Possível conflito de dados
```

**DECISÃO**: Opção A (SEPARADOS) é mais segura e mantém separação de responsabilidades.

---

## 📁 ARQUIVOS A CRIAR/MODIFICAR

```
PanoramaCP2B/
├── src/data/
│   ├── cp2b_macrodata.py                    (NOVO - dados do Jupyter)
│   └── residue_registry.py                  (MODIFICAR - adicionar referência)
│
├── src/ui/
│   ├── municipality_aggregation_chart.py    (NOVO)
│   ├── culture_distribution_sunburst.py     (NOVO)
│   ├── regional_heatmap_chart.py            (NOVO)
│   └── saf_validation_panel.py              (NOVO)
│
├── src/services/
│   ├── data_aggregator.py                   (NOVO)
│   └── municipality_ranker.py               (NOVO)
│
├── pages/
│   └── 5_📊_Panorama_SP.py                  (NOVO - nova página)
│
├── data/
│   └── cp2b_macrodata_backup.db             (BACKUP do Jupyter DB)
│
└── docs/
    ├── PHASE1_DIAGNOSTICO.md               (ESTE ARQUIVO)
    └── PAGE_ARCHITECTURE.md                (ATUALIZAR)
```

---

## 📊 MÉTRICAS FINAIS

| Métrica | Valor | Fonte |
|---------|-------|-------|
| Total Plantas | 425 | Jupyter DB ✅ |
| Municípios Cobertos | 184 | Jupyter DB ✅ |
| Potencial Total SP | 934M m³/ano | Jupyter DB ✅ |
| Potencial Médio/Planta | 2.2M m³/ano | 934M / 425 |
| Plantas Georreferenciadas | 200 (47%) | Jupyter DB ⚠️ |
| Tipos de Resíduo | 9 | Jupyter DB ✅ |
| Fatores SAF Validados | 9 | Google Earth Engine ✅ |
| Tabelas Conflitantes | 0 | Análise ✅ |

---

## ✅ STATUS PHASE 1

- [x] Identificar bancos disponíveis
- [x] Entender estrutura de cada banco
- [x] Analisar sobreposição de dados
- [x] Definir estratégia de integração
- [x] Criar plano de arquivos
- [x] Documentar decisões

**Resultado**: Pronto para Phase 2 (Integração)

---

## 🚀 PRÓXIMOS PASSOS

1. **Phase 2.1**: Copiar `cp2b_panorama.db` (Jupyter) como backup
2. **Phase 2.2**: Criar `src/data/cp2b_macrodata.py` com dados
3. **Phase 2.3**: Atualizar `src/data/residue_registry.py`
4. **Phase 3**: Criar visualizações com Plotly
5. **Phase 4**: Implementar Page 5 (Panorama SP)
