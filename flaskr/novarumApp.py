import os

import psycopg2
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
