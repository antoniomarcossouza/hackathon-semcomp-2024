import pandas as pd
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    session,
    make_response,
)
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import sql
import pickle

app = Flask(__name__, template_folder="templates")
app.secret_key = "wie4thingei4ohgah6Weegh5eifu7oow"  # You need this for sessions

load_dotenv("./conf/novarumApp.env")
database = os.getenv("DB_DATABASE")
user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost", database=database, user=user, password=password
    )
    return conn


# -----------------------
# Rotas da aplicação
# -----------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/validate_csv", methods=["GET", "POST"])
def validate_csv():
    # valida o csv e redireciona pra uma pagina de visualizacao dele
    return redirect(url_for("index"))


@app.route("/rules", methods=["GET", "POST"])
def rules():
    conn = get_db_connection()
    cur = conn.cursor()
    if conn and cur:
        cur.execute("SELECT * FROM regras;")
        rulelist = cur.fetchall()
    else:
        rulelist = ["Conexão com o banco falhou!"]
    cur.close()
    conn.close()
    if request.method == "GET":
        return render_template("rules/rules_table.html", rulelist=rulelist)
    # elif request.method == 'POST':
    #     if 'rule' in request.form.keys():
    #         rule = request.form.get('rule')
    #         if rule != '' :
    #             return render_template('rules/rules_submit.html')
    #         else:
    #             return 400


@app.route("/databases")
def databases():
    databaselist = ["dados 1", "dados 2", "dados 3"]
    return render_template("database/database_table.html", databaselist=databaselist)


@app.route("/create_database")
def create_database():

    if "df" in session and "df_name" in session:
        df = pickle.loads(session["df"])
        df_name = pickle.loads(session["df_name"])

        conn = get_db_connection()
        cur = conn.cursor()
        if conn and cur:

            #          QUERY para criar a tabela a partir dos nomes das colunas do CSV
            table_name = df_name
            columns = df.columns
            create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(
                    sql.SQL("{} TEXT").format(sql.Identifier(col)) for col in columns
                ),
            )
            cur.execute(create_table_query)
            print(df.iterrows())
            #           QUERY para inserir na tabela os valores
            for _, row in df.iterrows():
                insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    sql.Identifier(table_name),
                    sql.SQL(", ").join(map(sql.Identifier, df.columns)),
                    sql.SQL(", ").join(map(sql.Placeholder, df.columns)),
                )
                cur.execute(insert_query, tuple(row))
        else:
            response = make_response("Algum erro ocorreu ao conectar ao Banco\n")
            response.status_code = 500
            response.headers["Content-Type"] = "text/plain"
            return response
        conn.commit()
        cur.close()
        conn.close()
        print(f"Tabela '{table_name}' criada com sucesso e dados inseridos!")
        return df.to_html()
    else:
        response = make_response(
            "Missing Parameter! Arquivo nao enviado ou banco nao nomeado\n"
        )
        response.status_code = 400
        response.headers["Content-Type"] = "text/plain"
        return response


@app.route("/upload_database", methods=["GET", "POST"])
def upload_database():
    file = request.files["file"]
    df_name = request.form.get("df_name")
    session["df_name"] = pickle.dumps(df_name)
    if (
        file.content_type == "application/vnd.ms-excel"
        or file.content_type
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ):
        df = pd.read_excel(file)
        session["df"] = pickle.dumps(df)
        return redirect(url_for("create_database"))
        # return df.to_html()
    elif file.content_type == "text/csv":
        df = pd.read_csv(file)
        session["df"] = pickle.dumps(df)
        return redirect(url_for("create_database"))
        # return df.to_html()
    return render_template("database/database_table.html")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
