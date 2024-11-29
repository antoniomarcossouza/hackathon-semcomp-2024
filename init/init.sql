CREATE TABLE tb_regras (
    id serial PRIMARY KEY,
    nome_tabela VARCHAR(50) NOT NULL,
    texto TEXT NOT NULL,
    query TEXT NULL,
    last_updated date DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO tb_regras (nome_tabela, texto, query)
VALUES 
('tb_lactacao',
'O lançamento não pode ser 60% superior em relação à curva de uma raça em específico.',
'WITH cte_media_acumulada AS (
    SELECT
        atual.ano_semana,
        atual.data_inicio,
        atual.data_fim,
        atual.raca_holandesa_kg,
        atual.raca_jersey_kg,
        atual.raca_gir_kg,
        (
            SELECT AVG(anterior.raca_holandesa_kg)
            FROM tb_lactacao anterior
            WHERE anterior.data_fim < atual.data_inicio
        ) AS media_holandesa,
        (
            SELECT AVG(anterior.raca_jersey_kg)
            FROM tb_lactacao anterior
            WHERE anterior.data_fim < atual.data_inicio
        ) AS media_jersey,
        (
            SELECT AVG(anterior.raca_gir_kg)
            FROM tb_lactacao anterior
            WHERE anterior.data_fim < atual.data_inicio
        ) AS media_gir
    FROM
        tb_lactacao atual
)
SELECT
    ano_semana,
    data_inicio,
    data_fim,
    raca_holandesa_kg,
    media_holandesa,
    raca_jersey_kg,
    media_jersey,
    raca_gir_kg,
    media_gir
from cte_media_acumulada
WHERE
    (raca_holandesa_kg > 1.6 * media_jersey OR raca_holandesa_kg > 1.6 * media_gir OR
     raca_jersey_kg > 1.6 * media_holandesa OR raca_jersey_kg > 1.6 * media_gir OR
     raca_gir_kg > 1.6 * media_holandesa OR raca_gir_kg > 1.6 * media_jersey);'
),
(
'tb_lactacao',
'O lançamento não pode ser 30% superiores em relação à media dos lançamentos anteriores.',
'WITH cte_media_acumulada AS (
    SELECT
        atual.ano_semana,
        atual.data_inicio,
        atual.data_fim,
        atual.raca_holandesa_kg,
        atual.raca_jersey_kg,
        atual.raca_gir_kg,
        (
            SELECT AVG(anterior.raca_holandesa_kg)
            FROM tb_lactacao anterior
            WHERE anterior.data_fim < atual.data_inicio
        ) AS media_holandesa,
        (
            SELECT AVG(anterior.raca_jersey_kg)
            FROM tb_lactacao anterior
            WHERE anterior.data_fim < atual.data_inicio
        ) AS media_jersey,
        (
            SELECT AVG(anterior.raca_gir_kg)
            FROM tb_lactacao anterior
            WHERE anterior.data_fim < atual.data_inicio
        ) AS media_gir
    FROM
        tb_lactacao atual
)
SELECT
    ano_semana,
    data_inicio,
    data_fim,
    raca_holandesa_kg,
    media_holandesa,
    raca_jersey_kg,
    media_jersey,
    raca_gir_kg,
    media_gir
FROM
    cte_media_acumulada
WHERE
    (raca_holandesa_kg > 1.3 * media_holandesa AND media_holandesa IS NOT NULL) OR
    (raca_jersey_kg > 1.3 * media_jersey AND media_jersey IS NOT NULL) OR
    (raca_gir_kg > 1.3 * media_gir AND media_gir IS NOT NULL);'
),
(
'tb_lactacao',
'O lançamento não pode ser 40% superior ao lançamento anterior.',
'WITH cte_comparacao AS (
    SELECT
        atual.ano_semana AS semana_atual,
        anterior.ano_semana AS semana_anterior,
        atual.raca_holandesa_kg,
        anterior.raca_holandesa_kg AS raca_holandesa_kg_anterior,
        atual.raca_jersey_kg,
        anterior.raca_jersey_kg AS raca_jersey_kg_anterior,
        atual.raca_gir_kg,
        anterior.raca_gir_kg AS raca_gir_kg_anterior
    FROM
        tb_lactacao atual
    LEFT JOIN
        tb_lactacao anterior
    ON
        atual.data_inicio = anterior.data_fim + INTERVAL ''1 day''
)
SELECT
    semana_atual,
    semana_anterior,
    raca_holandesa_kg,
    raca_holandesa_kg_anterior,
    raca_jersey_kg,
    raca_jersey_kg_anterior,
    raca_gir_kg,
    raca_gir_kg_anterior
FROM
    cte_comparacao
WHERE
    raca_holandesa_kg > 1.4 * raca_holandesa_kg_anterior OR
    raca_jersey_kg > 1.4 * raca_jersey_kg_anterior OR
    raca_gir_kg > 1.4 * raca_gir_kg_anterior;'
);

CREATE TABLE tb_lactacao (
    ano_semana VARCHAR PRIMARY KEY,
    data_inicio DATE,
    data_fim DATE,
    raca_holandesa_kg NUMERIC(10, 2),
    raca_jersey_kg NUMERIC(10, 2),
    raca_gir_kg NUMERIC(10, 2)
);

INSERT INTO tb_lactacao (
    ano_semana,
    data_inicio,
    data_fim,
    raca_holandesa_kg,
    raca_jersey_kg,
    raca_gir_kg
)
VALUES
('2023_1', '2023-01-01', '2023-01-07', 10.00, 8.00, 6.40),
('2023_2', '2023-01-08', '2023-01-14', 15.00, 12.00, 9.60),
('2023_3', '2023-01-15', '2023-01-21', 20.00, 16.00, 12.80),
('2023_4', '2023-01-22', '2023-01-28', 25.00, 20.00, 16.00),
('2023_5', '2023-01-29', '2023-02-04', 28.00, 22.40, 17.92),
('2023_6', '2023-02-05', '2023-02-11', 30.00, 24.00, 19.20),
('2023_7', '2023-02-12', '2023-02-18', 36.00, 28.80, 23.04),
('2023_8', '2023-02-19', '2023-02-25', 40.00, 32.00, 25.60),
('2023_9', '2023-02-26', '2023-03-04', 42.00, 33.60, 26.88),
('2023_10', '2023-03-05', '2023-03-11', 44.00, 35.20, 28.16),
('2023_11', '2023-03-12', '2023-03-18', 45.00, 36.00, 28.80),
('2023_12', '2023-03-19', '2023-03-25', 46.00, 36.80, 29.44),
('2023_13', '2023-03-26', '2023-04-01', 45.00, 36.00, 28.80),
('2023_14', '2023-04-02', '2023-04-08', 44.50, 35.60, 28.48),
('2023_15', '2023-04-09', '2023-04-15', 43.50, 34.80, 27.84),
('2023_16', '2023-04-16', '2023-04-22', 43.00, 34.40, 27.52),
('2023_17', '2023-04-23', '2023-04-29', 42.00, 33.60, 26.88),
('2023_18', '2023-04-30', '2023-05-06', 41.00, 32.80, 26.24),
('2023_19', '2023-05-07', '2023-05-13', 40.00, 32.00, 25.60),
('2023_20', '2023-05-14', '2023-05-20', 39.00, 31.20, 24.96),
('2023_21', '2023-05-21', '2023-05-27', 38.00, 30.40, 24.32),
('2023_22', '2023-05-28', '2023-06-03', 37.00, 29.60, 23.68),
('2023_23', '2023-06-04', '2023-06-10', 36.00, 28.80, 23.04),
('2023_24', '2023-06-11', '2023-06-17', 34.90, 27.92, 22.34),
('2023_25', '2023-06-18', '2023-06-24', 33.80, 27.04, 21.63),
('2023_26', '2023-06-25', '2023-07-01', 32.70, 26.16, 20.93),
('2023_27', '2023-07-02', '2023-07-08', 31.60, 25.28, 20.22),
('2023_28', '2023-07-09', '2023-07-15', 30.50, 24.40, 18.72),
('2023_29', '2023-07-16', '2023-07-22', 29.40, 23.52, 17.22),
('2023_30', '2023-07-23', '2023-07-29', 28.30, 22.64, 15.72),
('2023_31', '2023-07-30', '2023-08-05', 27.20, 21.76, 14.22),
('2023_32', '2023-08-06', '2023-08-12', 26.10, 20.88, 12.72),
('2023_33', '2023-08-13', '2023-08-19', 25.00, 20.00, 11.22),
('2023_34', '2023-08-20', '2023-08-26', 23.90, 19.12, 9.72),
('2023_35', '2023-08-27', '2023-09-02', 22.80, 18.24, 8.22),
('2023_36', '2023-09-03', '2023-09-09', 21.70, 17.36, 6.72),
('2023_37', '2023-09-10', '2023-09-16', 20.60, 16.48, 5.22),
('2023_38', '2023-09-17', '2023-09-23', 19.50, 15.60, 0.00),
('2023_39', '2023-09-24', '2023-09-30', 18.40, 14.72, 0.00),
('2023_40', '2023-10-01', '2023-10-07', 17.30, 13.84, 0.00),
('2023_41', '2023-10-08', '2023-10-14', 16.20, 12.96, 0.00),
('2023_42', '2023-10-15', '2023-10-21', 15.10, 12.08, 0.00),
('2023_43', '2023-10-22', '2023-10-28', 14.00, 11.20, 0.00),
('2023_44', '2023-10-29', '2023-11-04', 12.90, 10.32, 0.00);

CREATE TABLE tb_violacoes (
    id_item VARCHAR NOT NULL,
    nome_tabela VARCHAR NOT NULL,
    id_regra_violada VARCHAR NOT NULL
);