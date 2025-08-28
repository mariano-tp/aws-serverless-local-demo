# Guía de Contribución

Gracias por tu interés 🙌. Este repo está pensado para ser simple y reproducible.

## Flujo de trabajo
1. **Abrí un issue** para proponer cambios de arquitectura o runtimes.
2. **Creá una rama** desde `main` (`feat/...`, `fix/...`, `docs/...`, `ci/...`).
3. **Commits** estilo *Conventional Commits*.
4. **Pull Request**:
   - Un tema por PR
   - Link al issue
   - Explicar qué servicios/variables de LocalStack cambian
   - Pasar todos los checks de CI

## Estilo / calidad
- Documentar arquitectura en README.
- Usar `/images` para diagramas si aplica.
- Mantener badges consistentes.

## CI
Los PRs deben quedar en **verde**:
- LocalStack levantado con `localstack/setup-localstack@v0`
- `terraform apply`
- Test de integración: subir a S3 y verificar item en DynamoDB
- `terraform destroy`

## Licencia
Al contribuir aceptás que tu aporte se publica bajo **MIT** (ver `LICENSE`).
