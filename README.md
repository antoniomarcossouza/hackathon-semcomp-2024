# Hackathon - Semana da Computação 2024

### Pré-requisitos
- Ter o `Python` instalado.[^1]
- Ter o `Poetry` instalado.[^2]
- Ter o `Docker` instalado.[^3]
- Ter uma conta no `Groq`.[^4]

## Como executar
- Copie o arquivo `conf/.env.example` para um `conf/.env` e configure a chave da API do Groq;
- Crie o banco de dados com `docker compose up -d`;
- Instale as dependências com `poetry install`;
- Execute a aplicação web com `python flaskr/novarumApp.py`;
- O Pipeline de dados pode ser encontrado em `notebooks/Pipeline.ipynb`.

[^1]: https://www.python.org/downloads/
[^2]: https://python-poetry.org/docs/#installation
[^3]: https://docs.docker.com/desktop
[^4]: https://groq.com/