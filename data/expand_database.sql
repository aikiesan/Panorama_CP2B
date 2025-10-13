-- Script para expandir o banco de dados cp2b_maps.db
-- Adiciona tabelas para suportar múltiplas fontes de dados

-- ============================================================================
-- TABELA: residuos_agricolas
-- Fonte: SIDRA/IBGE - Produção Agrícola Municipal
-- ============================================================================
CREATE TABLE IF NOT EXISTS residuos_agricolas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    cultura TEXT NOT NULL,
    area_plantada_ha REAL DEFAULT 0,
    producao_ton REAL DEFAULT 0,
    produtividade_ton_ha REAL DEFAULT 0,
    valor_producao_mil_reais REAL DEFAULT 0,
    residuo_gerado_ton REAL DEFAULT 0,
    fator_residuo_cultura REAL DEFAULT 0,
    potencial_biogas_m3 REAL DEFAULT 0,
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
);

CREATE INDEX IF NOT EXISTS idx_residuos_agricolas_mun ON residuos_agricolas(codigo_municipio);
CREATE INDEX IF NOT EXISTS idx_residuos_agricolas_cultura ON residuos_agricolas(cultura);
CREATE INDEX IF NOT EXISTS idx_residuos_agricolas_ano ON residuos_agricolas(ano);

-- ============================================================================
-- TABELA: residuos_pecuarios
-- Fonte: SIDRA/IBGE + Defesa Agropecuária SP - Efetivo de Rebanhos
-- ============================================================================
CREATE TABLE IF NOT EXISTS residuos_pecuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    tipo_criacao TEXT NOT NULL, -- 'Bovinos', 'Suínos', 'Aves', 'Piscicultura'
    num_cabecas REAL DEFAULT 0,
    peso_medio_kg REAL DEFAULT 0,
    residuo_kg_dia_cabeca REAL DEFAULT 0,
    residuo_ton_dia REAL DEFAULT 0,
    residuo_ton_ano REAL DEFAULT 0,
    potencial_biogas_m3_ano REAL DEFAULT 0,
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
);

CREATE INDEX IF NOT EXISTS idx_residuos_pecuarios_mun ON residuos_pecuarios(codigo_municipio);
CREATE INDEX IF NOT EXISTS idx_residuos_pecuarios_tipo ON residuos_pecuarios(tipo_criacao);
CREATE INDEX IF NOT EXISTS idx_residuos_pecuarios_ano ON residuos_pecuarios(ano);

-- ============================================================================
-- TABELA: residuos_urbanos
-- Fonte: SNIS (Sistema Nacional de Informações sobre Saneamento)
-- ============================================================================
CREATE TABLE IF NOT EXISTS residuos_urbanos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    populacao INTEGER DEFAULT 0,
    rsu_ton_ano REAL DEFAULT 0,
    rsu_per_capita_kg_dia REAL DEFAULT 0,
    coleta_seletiva_ton_ano REAL DEFAULT 0,
    organicos_ton_ano REAL DEFAULT 0,
    percentual_organicos REAL DEFAULT 0,
    aterro_sanitario BOOLEAN DEFAULT 0,
    poda_capina_ton_ano REAL DEFAULT 0,
    potencial_biogas_rsu_m3_ano REAL DEFAULT 0,
    potencial_biogas_poda_m3_ano REAL DEFAULT 0,
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
);

CREATE INDEX IF NOT EXISTS idx_residuos_urbanos_mun ON residuos_urbanos(codigo_municipio);
CREATE INDEX IF NOT EXISTS idx_residuos_urbanos_ano ON residuos_urbanos(ano);

-- ============================================================================
-- TABELA: residuos_industriais
-- Fonte: Dados industriais e agro-industriais
-- ============================================================================
CREATE TABLE IF NOT EXISTS residuos_industriais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    setor_industrial TEXT NOT NULL, -- 'Sucroalcooleiro', 'Frigorífico', 'Laticínio', etc.
    nome_estabelecimento TEXT,
    tipo_residuo TEXT,
    residuo_ton_ano REAL DEFAULT 0,
    composicao_organica_percentual REAL DEFAULT 0,
    potencial_biogas_m3_ano REAL DEFAULT 0,
    possui_tratamento BOOLEAN DEFAULT 0,
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
);

CREATE INDEX IF NOT EXISTS idx_residuos_industriais_mun ON residuos_industriais(codigo_municipio);
CREATE INDEX IF NOT EXISTS idx_residuos_industriais_setor ON residuos_industriais(setor_industrial);

-- ============================================================================
-- TABELA: dados_laboratoriais
-- Fonte: Referências técnicas e científicas
-- Parâmetros físico-químicos para caracterização de resíduos
-- ============================================================================
CREATE TABLE IF NOT EXISTS dados_laboratoriais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_residuo TEXT NOT NULL,
    parametro TEXT NOT NULL,
    valor_tipico TEXT,
    valor_min REAL,
    valor_max REAL,
    unidade TEXT,
    metodo TEXT,
    referencia TEXT,
    observacoes TEXT,
    data_atualizacao DATE DEFAULT CURRENT_DATE
);

CREATE INDEX IF NOT EXISTS idx_dados_lab_tipo ON dados_laboratoriais(tipo_residuo);
CREATE INDEX IF NOT EXISTS idx_dados_lab_parametro ON dados_laboratoriais(parametro);

-- ============================================================================
-- TABELA: dados_socioeconomicos
-- Fonte: IBGE - PIB Municipal, IDHM, indicadores sociais
-- ============================================================================
CREATE TABLE IF NOT EXISTS dados_socioeconomicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    pib_mil_reais REAL DEFAULT 0,
    pib_per_capita REAL DEFAULT 0,
    pib_agropecuaria_mil_reais REAL DEFAULT 0,
    pib_industria_mil_reais REAL DEFAULT 0,
    pib_servicos_mil_reais REAL DEFAULT 0,
    populacao INTEGER DEFAULT 0,
    idhm REAL,
    idhm_renda REAL,
    idhm_longevidade REAL,
    idhm_educacao REAL,
    gini REAL,
    emprego_formal INTEGER DEFAULT 0,
    renda_media REAL DEFAULT 0,
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
);

CREATE INDEX IF NOT EXISTS idx_socioeco_mun ON dados_socioeconomicos(codigo_municipio);
CREATE INDEX IF NOT EXISTS idx_socioeco_ano ON dados_socioeconomicos(ano);

-- ============================================================================
-- TABELA: uso_solo_mapbiomas
-- Fonte: MapBiomas - Cobertura e Uso do Solo
-- ============================================================================
CREATE TABLE IF NOT EXISTS uso_solo_mapbiomas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    classe_uso TEXT NOT NULL, -- 'Floresta', 'Agricultura', 'Pastagem', 'Urbano', etc.
    classe_nivel_1 TEXT,
    classe_nivel_2 TEXT,
    classe_nivel_3 TEXT,
    area_km2 REAL DEFAULT 0,
    area_ha REAL DEFAULT 0,
    percentual_territorio REAL DEFAULT 0,
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
);

CREATE INDEX IF NOT EXISTS idx_uso_solo_mun ON uso_solo_mapbiomas(codigo_municipio);
CREATE INDEX IF NOT EXISTS idx_uso_solo_ano ON uso_solo_mapbiomas(ano);
CREATE INDEX IF NOT EXISTS idx_uso_solo_classe ON uso_solo_mapbiomas(classe_uso);

-- ============================================================================
-- TABELA: defesa_agropecuaria
-- Fonte: Defesa Agropecuária do Estado de São Paulo
-- ============================================================================
CREATE TABLE IF NOT EXISTS defesa_agropecuaria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    propriedades_cadastradas INTEGER DEFAULT 0,
    area_inspecionada_ha REAL DEFAULT 0,
    estabelecimentos_certificados INTEGER DEFAULT 0,
    producao_organica BOOLEAN DEFAULT 0,
    rastreabilidade_animal BOOLEAN DEFAULT 0,
    gtps_emitidas INTEGER DEFAULT 0, -- Guias de Trânsito Pecuário
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
);

CREATE INDEX IF NOT EXISTS idx_defesa_agro_mun ON defesa_agropecuaria(codigo_municipio);
CREATE INDEX IF NOT EXISTS idx_defesa_agro_ano ON defesa_agropecuaria(ano);

-- ============================================================================
-- Fim do script
-- ============================================================================
