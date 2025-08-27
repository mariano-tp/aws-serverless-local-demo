[![ci: serverless](https://img.shields.io/github/actions/workflow/status/mariano-tp/aws-serverless-local-demo/serverless-ci.yml?branch=main&label=serverless-ci&style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/actions/workflows/serverless-ci.yml)
[![last commit](https://img.shields.io/github/last-commit/mariano-tp/aws-serverless-local-demo?style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/commits/main)
[![license: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)
[![stars](https://img.shields.io/github/stars/mariano-tp/aws-serverless-local-demo?style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/stargazers)

# AWS Serverless Local Demo

Demo **serverless** sin cuenta cloud usando:
- **AWS SAM** (Lambda + API Gateway) para levantar la API localmente (`sam local start-api`).
- **DynamoDB Local** via `docker-compose`.
- **Tests con `pytest` + `moto`** (sin levantar contenedores en CI).
- **CI en GitHub Actions**: lint, tests, `sam validate`, `cfn-lint`, y `docker compose config`.

> 100% local: no requiere credenciales AWS ni acceso a ninguna cuenta.

## Endpoints (local)
- `POST /todos` — body: `{"id":"1","title":"algo"}`
- `GET /todos/{id}` — devuelve el todo

## Ejecutar local

### 1) Dependencias de Python
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
