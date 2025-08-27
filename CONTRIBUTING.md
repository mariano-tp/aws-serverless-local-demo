# Guía de Contribución

Gracias por tu interés 🙌. Este repo está pensado para ser simple y reproducible.

## Flujo de trabajo
1. **Abrí un issue** usando la plantilla (Bug / Mejora), si aplica.
2. **Creá una rama** desde `main`:
   - `feat/<breve-descripcion>` para nuevas features
   - `fix/<breve-descripcion>` para bugs
   - `docs/...`, `ci/...` para documentación o pipelines
3. **Commits** estilo *Conventional Commits*:
   - `feat:`, `fix:`, `docs:`, `ci:`, `chore:`
4. **Pull Request**:
   - Un solo tema por PR
   - Link al issue
   - Pasar todos los checks de CI
   - Actualizar README/capturas si aplica

## Estilo / calidad
- Markdown simple y claro (español).
- Evitar archivos grandes en el repo (usar `/images` para capturas).
- Mantener consistencia de badges y secciones (README).

## CI
Los PRs deben quedar en **verde**:
- Linter / tests del proyecto (según repo).
- Validaciones (p.ej. `docker compose config`, `terraform fmt/validate`, `helm lint`, `pytest`, etc).

## Licencia
Al contribuir aceptás que tu aporte se publica bajo **MIT** (ver `LICENSE`).
