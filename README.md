[![ci](https://img.shields.io/github/actions/workflow/status/mariano-tp/aws-serverless-local-demo/ci.yml?branch=main&label=ci&style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/actions/workflows/ci.yml)
[![last commit](https://img.shields.io/github/last-commit/mariano-tp/aws-serverless-local-demo?style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/commits/main)
[![release](https://img.shields.io/github/v/release/mariano-tp/aws-serverless-local-demo?display_name=tag&style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/releases)
[![license: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)
[![stars](https://img.shields.io/github/stars/mariano-tp/aws-serverless-local-demo?style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/stargazers)


# AWS Serverless Local Demo

Demo serverless **AWS-like** sin cuenta cloud. Prueba el flujo **S3 → Lambda → DynamoDB** de forma local con **LocalStack** y CI en **GitHub Actions** (unit + integración).

## CI
- Levanta LocalStack como *service* (S3, SQS, DynamoDB).
- Hace *bootstrap*: bucket + queue + notificación S3→SQS + tabla DDB.
- Corre un test que sube un objeto, consume el evento de SQS y persiste en DDB.

## Ejecutar 100% online
1. Subí este repo a GitHub.
2. Abrí **Actions → ci → Run workflow**.
3. Debería quedar **verde** ✅.

## Correr local (opcional)
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

Ver también: [Código de Conducta](./CODE_OF_CONDUCT.md) · [Contribuir](./CONTRIBUTING.md) · [Seguridad](./SECURITY.md)
