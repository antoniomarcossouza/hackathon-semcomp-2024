import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
)

app = Flask(__name__, template_folder="templates")

load_dotenv("./conf/.env.example")
database = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
app.secret_key = os.getenv("APP_SECRET_KEY")

print(database, user, password, app.secret_key)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database=database,
        user=user,
        password=password,
    )
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/regras", methods=["GET", "POST"])
def rules():
    conn = get_db_connection()
    cur = conn.cursor()
    if conn and cur:
        cur.execute("SELECT * FROM tb_regras;")
        rulelist = cur.fetchall()
    else:
        rulelist = ["Conexão com o banco falhou!"]
    if request.method == "GET":
        cur.close()
        conn.close()
        return render_template("rules/rules_table.html", rulelist=rulelist, queryllm='Sua query será gerada aqui')
    elif request.method == 'POST':
        if 'texto' in request.form.keys() and 'nome_tabela' in request.form.keys():
            table_name = request.form.get('nome_tabela')
            rule = request.form.get('texto')
            action = request.form.get('action')
            if action=='saverule':
                insert_query = sql.SQL("INSERT INTO tb_regras (nome_tabela, texto) VALUES (%s, %s)")
                cur.execute(insert_query, (table_name, rule))
                conn.commit()
                return f"{table_name} e {rule} inseridos na tabela com sucesso!", 200

            elif action=='submitquery':
                # TODO LLM
                queryllm = rule
                return render_template("rules/rules_table.html", rulelist=rulelist, queryllm=queryllm)

        cur.close()
        conn.close()
        return render_template("rules/rules_table.html", rulelist=rulelist, queryllm='')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)