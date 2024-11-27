CREATE TABLE tb_regras (
    id serial PRIMARY KEY,
    nome_tabela varchar (50) NOT NULL,
    texto text NOT NULL,
    query text NULL,
    last_updated date DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO tb_regras (nome_tabela, texto)
VALUES (
        'tb_lactacao',
        'O lançamento não pode ser 40% superior em relação ao lançamento anterior'
    );
INSERT INTO tb_regras (nome_tabela, texto)
VALUES (
        'tb_lactacao',
        'O lançamento não pode ser 40% superior em relação ao lançamento anterior'
    );