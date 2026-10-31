# Convenciones de Git

## Ramas
- `main`: protegida. Sin commits directos. Siempre desplegable.
- `develop` (opcional): integración.
- `feature/<n>-<descripcion-corta>` · ej. `feature/12-salida-fefo`
- `bugfix/<n>-<descripcion>` · `docs/<descripcion>` · `test/<descripcion>`

Configurar en GitHub: *Settings → Branches → Branch protection* sobre `main`: exigir PR, 1 aprobación, y checks pasando.

## Commits (Conventional Commits)
`<tipo>(<alcance>): <descripción en imperativo>`

Tipos: `feat`, `fix`, `test`, `docs`, `refactor`, `style`, `chore`.

```
feat(inventory): sugerir lote por vencimiento más cercano
fix(catalog): normalizar código de producto a mayúsculas
test(inventory): cubrir salida con stock insuficiente
docs(readme): agregar variables de entorno
```
Commits pequeños y atómicos: un cambio lógico por commit. Referenciar la tarjeta en el cuerpo: `Refs #12`.

## Flujo
1. Tomar una tarjeta de «Listo» y pasarla a «En curso».
2. `git switch -c feature/12-salida-fefo` desde `main` actualizada.
3. Commits pequeños; `git push -u origin feature/12-salida-fefo`.
4. Abrir PR con la plantilla; pasar la tarjeta a «En revisión».
5. Otro integrante revisa (comentarios, aprobación). Nunca se aprueba el propio PR.
6. *Squash and merge* o merge normal; borrar la rama; tarjeta a «Hecho».

## Reglas de revisión
Revisar: lógica correcta, tests presentes, nombres claros, sin secretos, sin código muerto. Los comentarios son sobre el código, con sugerencias concretas.
