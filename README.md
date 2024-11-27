# Hackathon - Semana da Computação 2024

## Como executar

- No diretório raíz ativar o venv com o comando
  - `source .venv/bin/activate`
- Ainda no diretório raiz
  - `gunicorn --bind 0.0.0.0:5000 wsgi:app`

### Pré-requisitos
- Ter o `Poetry` instalado.[^1]
- Ter o `Docker` instalado.[^2]

[^1]: https://python-poetry.org/docs/#installation
[^2]: https://docs.docker.com/desktop