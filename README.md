[![ci](https://img.shields.io/github/actions/workflow/status/mariano-tp/aws-serverless-local-demo/ci.yml?branch=main&label=ci&style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/actions/workflows/ci.yml)
[![last commit](https://img.shields.io/github/last-commit/mariano-tp/aws-serverless-local-demo?style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/commits/main)
[![release](https://img.shields.io/github/v/release/mariano-tp/aws-serverless-local-demo?display_name=tag&style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/releases)
[![license: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)
[![stars](https://img.shields.io/github/stars/mariano-tp/aws-serverless-local-demo?style=flat-square)](https://github.com/mariano-tp/aws-serverless-local-demo/stargazers)

# AWS Serverless Local Demo

Demo de **arquitectura serverless** en AWS **100% local** (sin cuenta cloud) usando:

- **LocalStack** para emular servicios AWS (API Gateway, Lambda, DynamoDB, S3).
- **AWS SAM** para definir la infraestructura como código (IaC) en `template.yaml`.
- **Python 3.11** para la función Lambda.
- **GitHub Actions** para CI (validación del template + tests).

> Objetivo: poder **clonar → levantar → probar** sin credenciales de AWS y sin costos.

---

## Arquitectura

API Gateway (HTTP API) → Lambda (Python) → DynamoDB (+ S3 opcional para artefactos/logs).  
Todo definido en `template.yaml` y desplegado en LocalStack.

```
/
├── src/                  # Código de la Lambda (handler.py)
├── tests/                # Unit tests (pytest)
├── template.yaml         # SAM template (API, Lambda, DynamoDB, Roles)
├── docker-compose.yml    # LocalStack
└── .github/workflows/    # CI (sam validate + pytest)
```

---

## Requisitos

- Docker y Docker Compose
- Python 3.11 + pip
- **AWS SAM CLI** (para `sam validate` y ejecución local)
- **AWS CLI** (opcional) o `awslocal` (wrapper de LocalStack)

> Si usás **awslocal**, podés instalarlo con: `pip install awscli-local`

---

## Levantar en local (LocalStack)

1) Iniciar LocalStack:

```bash
docker compose up -d
# Esperar a que el contenedor localstack esté "healthy"
```

2) Desplegar la infraestructura y la Lambda en LocalStack usando CloudFormation:

```bash
# Opción A: usando awslocal (recomendado)
awslocal cloudformation deploy \
  --stack-name serverless-demo \
  --template-file template.yaml \
  --capabilities CAPABILITY_IAM
```

> TIP: si preferís **SAM local**, podés probar la Lambda sin LocalStack con:
> `sam build && sam local start-api` (expone http://127.0.0.1:3000).

3) Probar el endpoint (HTTP API). Para obtener el endpoint:

```bash
awslocal apigatewayv2 get-apis --query 'Items[0].ApiEndpoint' --output text
# Ejemplo de request (asumiendo ruta /items):
curl -s $(awslocal apigatewayv2 get-apis --query 'Items[0].ApiEndpoint' --output text)/items | jq
```

4) (Opcional) Consultar la tabla DynamoDB:

```bash
awslocal dynamodb list-tables
awslocal dynamodb scan --table-name ServerlessItems
```

---

## Ejecutar tests (unit tests)

```bash
pip install -r requirements.txt
pytest -q
```

---

## CI (GitHub Actions)

Este repo incluye un workflow `ci.yml` que ejecuta en cada push/PR:

- `sam validate` y (si está presente) `cfn-lint` sobre `template.yaml`  
- Instalación de dependencias y **pytest** sobre `src/` y `tests/`

Badges arriba del README muestran el estado del pipeline, último release y metadatos.

---

## Limpieza

```bash
# Borrar la pila (LocalStack)
awslocal cloudformation delete-stack --stack-name serverless-demo

# Apagar y limpiar LocalStack
docker compose down -v
```

---

## Rutas de ejemplo (sugeridas)

- `GET /items` — lista items desde DynamoDB.
- `POST /items` — inserta un item (JSON) en DynamoDB.
- `GET /health` — healthcheck simple.

> Si cambiás o agregás rutas, actualizá `template.yaml` (recursos + rutas) y el handler.

---

## Notas

- **Sin credenciales reales**: LocalStack no requiere claves de AWS (usa valores dummy).
- El template SAM es compatible con una cuenta real; si quisieras desplegarlo en AWS,
  ajustá parámetros/roles y reemplazá `awslocal` por `aws` apuntando a tu cuenta/region.

---

## Licencia

MIT — ver [`LICENSE`](./LICENSE).

## Créditos

Repositorio de portfolio por @mariano-tp. Construido para demostrar IaC (SAM), serverless y CI/Tests en un entorno **100% local**.

Ver también: [Código de Conducta](./CODE_OF_CONDUCT.md) · [Contribuir](./CONTRIBUTING.md) · [Seguridad](./SECURITY.md)
