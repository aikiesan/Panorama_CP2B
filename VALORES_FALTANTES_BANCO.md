# RELATÓRIO: VALORES FALTANTES NO BANCO DE DADOS

**Data:** 2025-10-20  
**Banco:** cp2b_panorama.db

---

## 📊 RESUMO DOS PROBLEMAS IDENTIFICADOS

### ✅ Valores Corretos (OK)
- **BMP**: 38/38 resíduos com valores corretos (< 1.0 m³/kg MS) ✅
- **TS (Sólidos Totais)**: 38/38 resíduos com valores ✅
- **C:N (Relação Carbono/Nitrogênio)**: 38/38 resíduos com valores ✅
- **CH4 (Teor de Metano)**: 38/38 resíduos com valores ✅
- **FC (Fator de Coleta)**: 38/38 resíduos com valores ✅
- **FCp (Fator de Competição)**: 38/38 resíduos com valores ✅

### ❌ Valores Faltantes (PROBLEMA)

#### 1. **VS (Sólidos Voláteis)** - 8 resíduos com NULL
```
- Bagaço de cana
- Bagaço de malte
- Casca de café
- Casca de milho
- Dejetos frescos de aves
- Mucilagem de café
- Torta de filtro
- Vinhaça
```

**Impacto:** MÉDIO  
**Solução:** Preencher com valores típicos da literatura ou deixar NULL (o webapp deve tratar)

---

#### 2. **FS (Fator Sazonalidade)** - 38/38 resíduos com NULL
**Impacto:** ALTO - Afeta cálculo de disponibilidade  
**Valores típicos:**
- Produção contínua (urbano, industrial): 1.0
- Semi-contínuo (pecuária): 0.95
- Sazonal moderado (agricultura perene): 0.85
- Sazonal concentrado (agricultura anual): 0.70

---

#### 3. **FL (Fator Logístico)** - 38/38 resíduos com NULL
**Impacto:** ALTO - Afeta cálculo de disponibilidade  
**Valores típicos:**
- Concentrado (usinas, frigoríficos): 1.0
- Moderado (fazendas médias): 0.90
- Disperso (pequenas propriedades): 0.75
- Muito disperso (urbano distribuído): 0.65

---

## 🔍 ANÁLISE DETALHADA

### Valores Médios Atuais
```
Total de resíduos: 38
TS médio: 40.39%
VS médio: 79.92% (apenas 30 resíduos)
C:N médio: 26.28
CH4 médio: 60.88%
FC médio: 0.6121
FCp médio: 0.2226
FS médio: NULL (todos)
FL médio: NULL (todos)
```

### Distribuição de Disponibilidade Final
Apesar de FS e FL serem NULL, há valores de `disponibilidade_final_media`:
- Mínimo: 0.03%
- Médio: ~20-30%
- Máximo: ~80%

**Nota:** Esses valores foram calculados sem FS e FL, ou com valores padrão implícitos.

---

## 🛠️ SOLUÇÕES PROPOSTAS

### Solução 1: Valores Padrão no Loader (IMPLEMENTADO)
No `database_loader.py`, já tratamos valores NULL:

```python
fs=row['fs_medio'] or 1.0,  # Padrão: sem sazonalidade
fl=row['fl_medio'] or 1.0,  # Padrão: sem restrição logística
```

**Status:** ✅ Implementado

---

### Solução 2: Popular FS e FL no Banco (RECOMENDADO)

#### Script SQL para popular valores típicos:

```sql
-- Popular FS (Fator Sazonalidade) por setor
UPDATE fatores_disponibilidade
SET fs_medio = CASE 
    WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'UR_URBANO' THEN 1.0
    WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'IN_INDUSTRIAL' THEN 0.95
    WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'PC_PECUARIA' THEN 0.90
    WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'AG_AGRICULTURA' THEN 0.75
    ELSE 0.85
END,
fs_min = fs_medio * 0.8,
fs_max = LEAST(fs_medio * 1.2, 1.0);

-- Popular FL (Fator Logístico) por setor
UPDATE fatores_disponibilidade
SET fl_medio = CASE 
    WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'IN_INDUSTRIAL' THEN 0.95
    WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'UR_URBANO' THEN 0.80
    WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'PC_PECUARIA' THEN 0.85
    WHEN (SELECT setor FROM residuos WHERE id = residuo_id) = 'AG_AGRICULTURA' THEN 0.75
    ELSE 0.80
END,
fl_min = fl_medio * 0.8,
fl_max = LEAST(fl_medio * 1.2, 1.0);
```

---

### Solução 3: Popular VS faltantes

```sql
-- Valores típicos de VS para resíduos específicos
UPDATE parametros_quimicos
SET vs_medio = CASE 
    WHEN residuo_id IN (SELECT id FROM residuos WHERE nome = 'Bagaço de cana') THEN 90.0
    WHEN residuo_id IN (SELECT id FROM residuos WHERE nome = 'Vinhaça') THEN 85.0
    WHEN residuo_id IN (SELECT id FROM residuos WHERE nome = 'Torta de filtro') THEN 82.0
    WHEN residuo_id IN (SELECT id FROM residuos WHERE nome = 'Casca de café') THEN 88.0
    WHEN residuo_id IN (SELECT id FROM residuos WHERE nome = 'Casca de milho') THEN 85.0
    WHEN residuo_id IN (SELECT id FROM residuos WHERE nome = 'Mucilagem de café') THEN 83.0
    WHEN residuo_id IN (SELECT id FROM residuos WHERE nome = 'Bagaço de malte') THEN 87.0
    WHEN residuo_id IN (SELECT id FROM residuos WHERE nome = 'Dejetos frescos de aves') THEN 75.0
    ELSE vs_medio
END,
vs_min = vs_medio * 0.85,
vs_max = vs_medio * 1.15
WHERE vs_medio IS NULL;
```

---

## ✅ STATUS ATUAL NO WEBAPP

### O que está funcionando:
✅ BMP carregando corretamente  
✅ TS carregando corretamente  
✅ C:N carregando corretamente  
✅ FC e FCp carregando corretamente  
✅ Disponibilidade final tem valores (calculados previamente)  

### O que pode ter problemas:
⚠️ VS faltando para 8 resíduos (exibir como "N/A")  
⚠️ FS e FL não disponíveis individualmente (usa padrão 1.0)  
⚠️ Cálculos que dependem de FS/FL podem estar simplificados  

---

## 🎯 RECOMENDAÇÕES

### Curto Prazo (Urgente)
1. ✅ **Loader já trata NULL** - Usa valores padrão
2. ✅ **Webapp funciona** - Não quebra com valores NULL

### Médio Prazo (Melhoria)
1. **Popular FS e FL no banco** com valores típicos por setor
2. **Popular VS faltantes** com valores da literatura
3. **Adicionar ranges** (min/max) para FS e FL

### Longo Prazo (Ideal)
1. **Validar valores** com especialistas do CP2B
2. **Criar interface de edição** no webapp
3. **Documentar fontes** de cada valor

---

## 📝 CONCLUSÃO

**O banco está funcional para uso no webapp**, mas poderia ser melhorado com:
- Valores de FS e FL populados
- VS completado para todos os resíduos
- Documentação das fontes de dados

**Prioridade:**
- 🔴 ALTA: Popular FS e FL (afeta cálculos de disponibilidade)
- 🟡 MÉDIA: Popular VS faltantes (afeta alguns cálculos)
- 🟢 BAIXA: Adicionar ranges e documentação

---

**Última atualização:** 2025-10-20 15:00

