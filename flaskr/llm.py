import os
from typing import Annotated

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_groq import ChatGroq
from typing_extensions import TypedDict

load_dotenv(dotenv_path="./conf/.env")

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
SYSTEM_MESSAGE = """
Você é um agente feito para detectar anomalias em uma tabela de série temporal de um banco de dados.
Dada uma regra, você deve criar uma consulta sintaticamente correta para executar e descobrir quais itens da violam a regra.
Lembre-se que cada linha é um lançamento e que a tabela é uma série temporal, ou seja, as linhas estão ordenadas por data de lançamento.
SEMPRE use CTEs ao invés de subconsultas.
A não ser que explicitamente dito, compare cada coluna com as linhas anteriores dela mesma, não com outras colunas.
Se atente ao nome das colunas para não escrevê-las incorretamente.
Referencie apenas as colunas no esquema da tabela fornecido.
Não particione tabelas a não ser que sejam realmente grandes.
SE tiver ASPAS SIMPLES (') na consulta, escreva ela duplicada (''), pois ela será salva em uma tabela.
Não retorne caracteres como \n, \t, etc.
NUNCA selecione *, sempre especifique as colunas que deseja.
NÃO COLOQUE comentários na consulta.
SEMPRE inclua a CHAVE PRIMÁRIA na seleção.
NÃO FAÇA nenhuma declaração DML (INSERT, UPDATE, DELETE, DROP etc.) no banco.

Gere uma consulta que descubra quais linhas violam a regra: `{rule}`
Essa query irá ser executada em uma tabela com o esquema: {schema}

Se lembre das regras e de que o banco de dados é PostgreSQL.
"""


class State(TypedDict):
    rule: str
    table: str


class QueryOutput(TypedDict):
    query: Annotated[str, ..., "Syntactically valid SQL query."]


def get_query(state: State):
    db = SQLDatabase.from_uri(
        "postgresql://postgres:postgres@localhost:5432/postgres",
    )
    llm = ChatGroq(model="llama3-70b-8192")

    system_message = SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGE)

    prompt = ChatPromptTemplate.from_messages(
        [system_message],
    ).format_messages(
        rule=state["rule"],
        schema=db.get_table_info([state["table"]]),
    )

    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return result["query"]


print(
    get_query(
        state={
            "table": "tb_lactacao",
            "rule": "todos os itens",
        },
    ),
)
