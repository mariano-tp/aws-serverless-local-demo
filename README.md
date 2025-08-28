# AWS Serverless Local Demo (sin cuenta cloud)

Demo mínima de **S3 → SQS → DynamoDB** usando **LocalStack (OSS)** y **GitHub Actions**.
No usa Lambda (para evitar límites de OSS); el test integra el flujo simulando el "worker".

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
