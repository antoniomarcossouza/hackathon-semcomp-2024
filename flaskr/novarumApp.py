import os

import psycopg2
import sqlfluff
from dotenv import load_dotenv
from flask import Flask, render_template, request
from llm import get_query
from psycopg2 import sql

load_dotenv(dotenv_path="./conf/.env")


app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("APP_SECRET_KEY")

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/graphs")
def graphs():
    conn = get_db_connection()
    cur = conn.cursor()
    if conn and cur:
        cur.execute("SELECT * FROM tb_regras;")
        rulelist = cur.fetchall()
    else:
        rulelist = ["Conexão com o banco falhou!"]

    cur.close()
    conn.close()
    return render_template("rules/graphs_page.html", rulelist=rulelist)


def get_rules(conn, cursor):
    if conn and cursor:
        cursor.execute("SELECT * FROM tb_regras;")
        return cursor.fetchall()
    return ["Conexão com o banco falhou!"]


@app.route("/regras", methods=["GET", "POST"])
def rules():
    conn = get_db_connection()
    cur = conn.cursor()
    rulelist = get_rules(conn, cur)

    if request.method == "GET":
        cur.close()
        conn.close()
        return render_template(
            "rules/rules_table.html",
            rulelist=rulelist,
            queryllm="Sua query será gerada aqui",
        )
    if request.method == "POST":
        global query
        if (
            "texto" in request.form.keys()
            and "nome_tabela" in request.form.keys()
        ):
            table_name = request.form.get("nome_tabela")
            rule = request.form.get("texto")
            action = request.form.get("action")
            if action == "saverule":
                insert_query = sql.SQL(
                    "INSERT INTO tb_regras (nome_tabela, texto, query) VALUES (%s, %s, %s)",
                )
                cur.execute(insert_query, (table_name, rule, query))
                conn.commit()
                return render_template(
                    "rules/rules_table.html",
                    rulelist=get_rules(conn, cur),
                    queryllm="Sua query será gerada aqui",
                )
            if action == "submitquery":
                cur.execute(sql.SQL("SELECT to_regclass(%s);"), [table_name])
                table_exists = cur.fetchone()[0] is not None

                if not table_exists:
                    return render_template(
                        "rules/rules_table.html",
                        rulelist=rulelist,
                        queryllm=f"A tabela '{table_name}' não existe no banco de dados.",
                    )

                query = get_query(
                    state={
                        "table": table_name,
                        "rule": rule,
                    },
                )
                return render_template(
                    "rules/rules_table.html",
                    rulelist=rulelist,
                    queryllm=sqlfluff.fix(query, dialect="postgres"),
                )

        cur.close()
        conn.close()
        return render_template(
            "rules/rules_table.html",
            rulelist=rulelist,
            queryllm="",
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
