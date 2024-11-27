CREATE TABLE tb_lactacao (
    ano INT,
    semana INT,
    data_inicio DATE,
    data_fim DATE,
    raca_holandesa_kg NUMERIC(10, 2),
    raca_jersey_kg NUMERIC(10, 2),
    raca_gir_kg NUMERIC(10, 2)
);

INSERT INTO tb_lactacao (
    ano,
    semana,
    data_inicio,
    data_fim,
    raca_holandesa_kg,
    raca_jersey_kg,
    raca_gir_kg
)
VALUES
(2023, 1, '2023-01-01', '2023-01-07', 10.00, 8.00, 6.40),
(2023, 2, '2023-01-08', '2023-01-14', 15.00, 12.00, 9.60),
(2023, 3, '2023-01-15', '2023-01-21', 20.00, 16.00, 12.80),
(2023, 4, '2023-01-22', '2023-01-28', 25.00, 20.00, 16.00),
(2023, 5, '2023-01-29', '2023-02-04', 28.00, 22.40, 17.92),
(2023, 6, '2023-02-05', '2023-02-11', 30.00, 24.00, 19.20),
(2023, 7, '2023-02-12', '2023-02-18', 36.00, 28.80, 23.04),
(2023, 8, '2023-02-19', '2023-02-25', 40.00, 32.00, 25.60),
(2023, 9, '2023-02-26', '2023-03-04', 42.00, 33.60, 26.88),
(2023, 10, '2023-03-05', '2023-03-11', 44.00, 35.20, 28.16),
(2023, 11, '2023-03-12', '2023-03-18', 45.00, 36.00, 28.80),
(2023, 12, '2023-03-19', '2023-03-25', 46.00, 36.80, 29.44),
(2023, 13, '2023-03-26', '2023-04-01', 45.00, 36.00, 28.80),
(2023, 14, '2023-04-02', '2023-04-08', 44.50, 35.60, 28.48),
(2023, 15, '2023-04-09', '2023-04-15', 43.50, 34.80, 27.84),
(2023, 16, '2023-04-16', '2023-04-22', 43.00, 34.40, 27.52),
(2023, 17, '2023-04-23', '2023-04-29', 42.00, 33.60, 26.88),
(2023, 18, '2023-04-30', '2023-05-06', 41.00, 32.80, 26.24),
(2023, 19, '2023-05-07', '2023-05-13', 40.00, 32.00, 25.60),
(2023, 20, '2023-05-14', '2023-05-20', 39.00, 31.20, 24.96),
(2023, 21, '2023-05-21', '2023-05-27', 38.00, 30.40, 24.32),
(2023, 22, '2023-05-28', '2023-06-03', 37.00, 29.60, 23.68),
(2023, 23, '2023-06-04', '2023-06-10', 36.00, 28.80, 23.04),
(2023, 24, '2023-06-11', '2023-06-17', 34.90, 27.92, 22.34),
(2023, 25, '2023-06-18', '2023-06-24', 33.80, 27.04, 21.63),
(2023, 26, '2023-06-25', '2023-07-01', 32.70, 26.16, 20.93),
(2023, 27, '2023-07-02', '2023-07-08', 31.60, 25.28, 20.22),
(2023, 28, '2023-07-09', '2023-07-15', 30.50, 24.40, 18.72),
(2023, 29, '2023-07-16', '2023-07-22', 29.40, 23.52, 17.22),
(2023, 30, '2023-07-23', '2023-07-29', 28.30, 22.64, 15.72),
(2023, 31, '2023-07-30', '2023-08-05', 27.20, 21.76, 14.22),
(2023, 32, '2023-08-06', '2023-08-12', 26.10, 20.88, 12.72),
(2023, 33, '2023-08-13', '2023-08-19', 25.00, 20.00, 11.22),
(2023, 34, '2023-08-20', '2023-08-26', 23.90, 19.12, 9.72),
(2023, 35, '2023-08-27', '2023-09-02', 22.80, 18.24, 8.22),
(2023, 36, '2023-09-03', '2023-09-09', 21.70, 17.36, 6.72),
(2023, 37, '2023-09-10', '2023-09-16', 20.60, 16.48, 5.22),
(2023, 38, '2023-09-17', '2023-09-23', 19.50, 15.60, 0.00),
(2023, 39, '2023-09-24', '2023-09-30', 18.40, 14.72, 0.00),
(2023, 40, '2023-10-01', '2023-10-07', 17.30, 13.84, 0.00),
(2023, 41, '2023-10-08', '2023-10-14', 16.20, 12.96, 0.00),
(2023, 42, '2023-10-15', '2023-10-21', 15.10, 12.08, 0.00),
(2023, 43, '2023-10-22', '2023-10-28', 14.00, 11.20, 0.00),
(2023, 44, '2023-10-29', '2023-11-04', 12.90, 10.32, 0.00);