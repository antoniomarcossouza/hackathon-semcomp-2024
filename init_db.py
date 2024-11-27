from dotenv import load_dotenv
import os
import psycopg2

load_dotenv('./conf/novarumApp.env')
database=os.getenv('DB_DATABASE')
user=os.getenv('DB_USERNAME')
password=os.getenv('DB_PASSWORD')

conn = psycopg2.connect(
        host="localhost",
        database=database,
        user=user,
        password=password)

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS regras;')

cur.execute('CREATE TABLE regras (id serial PRIMARY KEY,'
                                 'nome_tb_aplicada varchar (50) NOT NULL,'
                                 'texto text NOT NULL,'
                                 'last_updated date DEFAULT CURRENT_TIMESTAMP);'
                                 )

cur.execute('INSERT INTO regras (nome_tb_aplicada, texto)'
            'VALUES (%s, %s)',
            ('peso_bovino',
             'O lançamento não pode ser 50% superior em relação à curva de uma raça em específico')
            )
cur.execute('INSERT INTO regras (nome_tb_aplicada, texto)'
            'VALUES (%s, %s)',
            ('peso_bovino',
             'O lançamento não pode ser 40% superior em relação ao lançamento anterior')
            )

conn.commit()

cur.close()
conn.close()