import pandas as pd
from flask import Flask, render_template, url_for, redirect, request
from dotenv import load_dotenv
import os
import psycopg2

app = Flask(__name__, template_folder='templates')

#-----------------------
# Carrega as variaveis de ambiente
#-----------------------
load_dotenv('./conf/novarumApp.env')
database=os.getenv('DB_DATABASE')
user=os.getenv('DB_USERNAME')
password=os.getenv('DB_PASSWORD')

#-----------------------
# Inicia conexão com o BD
#-----------------------
def get_db_connection():
    conn = psycopg2.connect(
            host="localhost",
            database=database,
            user=user,
            password=password)
    return conn

#-----------------------
# Rotas da aplicação
#-----------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate_csv', methods=['GET', 'POST'])
def validate_csv():
    # valida o csv e redireciona pra uma pagina de visualizacao dele
    return redirect(url_for('index'))

@app.route('/rules', methods=['GET', 'POST'])
def rules():
    conn = get_db_connection()
    cur = conn.cursor()
    if conn and cur:
        cur.execute('SELECT * FROM regras;')
        rulelist = cur.fetchall()
    else:
        rulelist = ['Conexão com o banco falhou!']
    cur.close()
    conn.close()
    if request.method == 'GET':
        return render_template('rules/rules_table.html', rulelist=rulelist)
    # elif request.method == 'POST':
    #     if 'rule' in request.form.keys():
    #         rule = request.form.get('rule')
    #         if rule != '' :
    #             return render_template('rules/rules_submit.html')
    #         else:
    #             return 400

@app.route('/databases')
def databases():
    databaselist = ['dados 1', 'dados 2', 'dados 3']
    return render_template('database/database_table.html', databaselist=databaselist)


@app.route('/upload_database', methods=['GET','POST'])
def upload_database():
    file = request.files['file']

    if file.content_type == 'application/vnd.ms-excel' or file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(file)
        return df.to_html()
    elif file.content_type == 'text/csv':
        df = pd.read_csv(file)
        return df.to_html()
    return render_template('database/database_table.html')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)