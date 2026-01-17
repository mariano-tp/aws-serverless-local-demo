> Available languages / Idiomas disponibles: [*English*](README.md) / [*Español*](README.ES.md)

[![ci](https://img.shields.io/github/actions/workflow/status/mariano-tp/aws-serverless-local-demo/ci.yml?branch=main&label=ci&style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/actions/workflows/ci.yml)
[![last commit](https://img.shields.io/github/last-commit/mariano-tp/aws-serverless-local-demo?style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/commits/main)
[![release](https://img.shields.io/github/v/release/mariano-tp/aws-serverless-local-demo?display_name=tag&style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/releases)
[![license: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)
[![stars](https://img.shields.io/github/stars/mariano-tp/aws-serverless-local-demo?style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/stargazers)

# AWS Serverless Local Demo

Demo tipo serverless (estilo AWS) sin necesidad de cuenta cloud. Valida el flujo S3 → Lambda → DynamoDB usando LocalStack y CI en GitHub Actions (tests unitarios + de integración).

## Qué se valida en CI (GitHub Actions)
- Levanta LocalStack como servicio (S3, SQS, DynamoDB)
- Inicializa recursos: bucket, cola, notificación S3→SQS y tabla en DDB
- Ejecuta un test de integración que sube un objeto, consume el evento desde SQS y lo persiste en DynamoDB

## Validación 100% online (GitHub Actions)
1. Subí este repo a GitHub
2. Entrá a Actions → ci → Run workflow
3. El workflow debería quedar en verde

## Ejecución local (opcional)
```bash
docker compose up -d
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1
pytest -q
```

## Estructura
```
.
├── .github/workflows/ci.yml
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── tests/
    └── integration/
        └── test_flow_localstack.py
```

## Créditos

Repositorio de portfolio por @mariano-tp. Licencia MIT.

Ver también: [Code of Conduct](./CODE_OF_CONDUCT.md) · [Contributing](./CONTRIBUTING.md) · [Security](./SECURITY.md)


docker compose up -d
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1
pytest -q
