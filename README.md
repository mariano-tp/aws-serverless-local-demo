> Available languages / Idiomas disponibles: [*English*](README.md) / [*Español*](README.ES.md)

[![ci](https://img.shields.io/github/actions/workflow/status/mariano-tp/aws-serverless-local-demo/ci.yml?branch=main&label=ci&style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/actions/workflows/ci.yml)
[![last commit](https://img.shields.io/github/last-commit/mariano-tp/aws-serverless-local-demo?style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/commits/main)
[![release](https://img.shields.io/github/v/release/mariano-tp/aws-serverless-local-demo?display_name=tag&style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/releases)
[![license: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)
[![stars](https://img.shields.io/github/stars/mariano-tp/aws-serverless-local-demo?style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/stargazers)


# AWS Serverless Local Demo

Serverless **AWS-like** demo without a cloud account. Test the **S3 → Lambda → DynamoDB** flow locally with **LocalStack** and CI in **GitHub Actions** (unit + integration).

## CI
- Spins up LocalStack as a *service* (S3, SQS, DynamoDB).
- Bootstraps resources: bucket + queue + S3→SQS notification + DDB table.
- Runs a test that uploads an object, consumes the SQS event, and persists it in DDB.

## Run 100% online
1. Push this repo to GitHub.
2. Go to **Actions → ci → Run workflow**.
3. The workflow should turn **green**.

## Run locally (optional)
```bash
docker compose up -d
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1
pytest -q
```

## Structure
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

## Credits
Portfolio repository by @mariano-tp. Licensed under MIT.

See also: [Code of Conduct](./CODE_OF_CONDUCT.md) · [Contributing](./CONTRIBUTING.md) · [Security](./SECURITY.md)
