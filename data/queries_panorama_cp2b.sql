
-- ============================================================================
-- QUERIES ÚTEIS PARA O PANORAMA CP2B
-- ============================================================================

-- 1. LISTAR TODOS OS RESÍDUOS COM RANGES COMPLETOS
SELECT 
    r.codigo,
    r.nome,
    r.setor,
    p.bmp_medio || ' (' || p.bmp_min || '-' || p.bmp_max || ') ' || p.bmp_unidade as BMP_Range,
    p.ts_medio || ' (' || p.ts_min || '-' || p.ts_max || ') %' as TS_Range,
    p.vs_medio || ' (' || p.vs_min || '-' || p.vs_max || ') %' as VS_Range,
    f.fc_medio || ' (' || f.fc_min || '-' || f.fc_max || ')' as FC_Range
FROM residuos r
LEFT JOIN parametros_quimicos p ON r.id = p.residuo_id
LEFT JOIN fatores_disponibilidade f ON r.id = f.residuo_id
ORDER BY r.setor, r.nome;

-- 2. CALCULAR POTENCIAL MÉDIO/MIN/MAX POR SETOR
SELECT 
    r.setor,
    COUNT(*) as num_residuos,
    AVG(p.bmp_medio) as bmp_medio_setor,
    MIN(p.bmp_min) as bmp_min_setor,
    MAX(p.bmp_max) as bmp_max_setor
FROM residuos r
JOIN parametros_quimicos p ON r.id = p.residuo_id
GROUP BY r.setor;

-- 3. RESÍDUOS COM MAIOR POTENCIAL (TOP 10)
SELECT 
    r.nome,
    r.setor,
    p.bmp_max as potencial_maximo,
    p.bmp_medio as potencial_medio,
    p.bmp_unidade
FROM residuos r
JOIN parametros_quimicos p ON r.id = p.residuo_id
WHERE p.bmp_max IS NOT NULL
ORDER BY p.bmp_max DESC
LIMIT 10;

-- 4. BUSCAR RESÍDUO ESPECÍFICO COM TODOS OS DADOS
SELECT 
    r.*,
    p.*,
    f.*
FROM residuos r
LEFT JOIN parametros_quimicos p ON r.id = p.residuo_id
LEFT JOIN fatores_disponibilidade f ON r.id = f.residuo_id
WHERE r.codigo = 'PALHA'; -- Exemplo: PALHA de cana

-- 5. CRIAR VIEW PARA WEBAPP (Dados prontos para visualização)
CREATE VIEW IF NOT EXISTS vw_residuos_completo AS
SELECT 
    r.codigo,
    r.nome,
    r.setor,
    r.categoria_nome,
    r.icon,
    p.bmp_medio, p.bmp_min, p.bmp_max, p.bmp_unidade,
    p.ts_medio, p.ts_min, p.ts_max,
    p.vs_medio, p.vs_min, p.vs_max,
    p.cn_medio, p.cn_min, p.cn_max,
    p.ch4_medio, p.ch4_min, p.ch4_max,
    f.fc_medio, f.fc_min, f.fc_max,
    f.fcp_medio, f.fcp_min, f.fcp_max,
    f.disponibilidade_final_media,
    p.nivel_confianca,
    p.validado
FROM residuos r
LEFT JOIN parametros_quimicos p ON r.id = p.residuo_id
LEFT JOIN fatores_disponibilidade f ON r.id = f.residuo_id;

-- 6. QUERY PARA API JSON (Formato para webapp)
SELECT json_object(
    'codigo', r.codigo,
    'nome', r.nome,
    'setor', r.setor,
    'parametros', json_object(
        'bmp', json_object('medio', p.bmp_medio, 'min', p.bmp_min, 'max', p.bmp_max),
        'ts', json_object('medio', p.ts_medio, 'min', p.ts_min, 'max', p.ts_max),
        'vs', json_object('medio', p.vs_medio, 'min', p.vs_min, 'max', p.vs_max)
    ),
    'fatores', json_object(
        'fc', json_object('medio', f.fc_medio, 'min', f.fc_min, 'max', f.fc_max),
        'fcp', json_object('medio', f.fcp_medio, 'min', f.fcp_min, 'max', f.fcp_max)
    )
) as json_data
FROM residuos r
LEFT JOIN parametros_quimicos p ON r.id = p.residuo_id
LEFT JOIN fatores_disponibilidade f ON r.id = f.residuo_id;
