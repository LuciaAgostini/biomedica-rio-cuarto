# Tablero Kanban (proyecto individual)

Herramienta: **GitHub Projects**. Columnas: `Backlog · Listo · En curso · En revisión · Hecho`.
Reglas: máximo 2 tarjetas «En curso» a la vez; cada PR cita su tarjeta (`Cierra #n`); nada se commitea directo a `main`.

## Alcance recomendado para una persona
**Dentro del MVP:** HU-01, 02, 04, 07, 08, 09, 10, 12, 13, 14, 16, 17, 18 y el rol Superadministrador con HU-03 (usuarios) y HU-05 (categorías).
**Fuera (mejora futura):** HU-06 (filtros avanzados), HU-11 (stock bajo), HU-15 (registro de actividad). Si sobra tiempo, HU-11 es la más barata.
Entidades CRUD vinculadas: Producto, Proveedor y Lote (cumple las 3 exigidas).

## Sprint 0 · Fundaciones
- Crear repo, proteger `main`, plantilla de PR, tablero
- Django + PostgreSQL + `.env` + ruff + pytest
- Usuario con roles + login/logout (HU-01, HU-02)
- Layout base con identidad Biomédica (HU-17)

## Sprint 1 · Catálogo y proveedores
- Revisar y entender el módulo Producto de referencia (HU-04)
- CRUD Categorías, solo Superadmin (HU-05)
- CRUD Proveedores (HU-07)
- Gestión de usuarios (HU-03) y tests de permisos (RN-13)

## Sprint 2 · Núcleo de inventario
- Modelos Lote y MovimientoStock + migraciones + constraints
- `registrar_entrada` + tests RN-01..04 (HU-08)
- `registrar_salida` con FEFO + tests RN-05..07, RN-12 (HU-09)
- Stock por producto + test RN-08 (HU-10)
- Historial de movimientos (HU-13)

## Sprint 3 · Vencimientos, API y cierre
- Próximos a vencer + parámetro de días + test RN-10 (HU-12, HU-14)
- Endpoints DRF + Swagger (HU-18)
- Deploy en la nube
- Pruebas manuales, checklist final, README, demo

## Cómo cubrir lo "colaborativo" trabajando sola
- Usá ramas y PRs igual que en equipo, con la plantilla completa. Es lo que evidencia el proceso.
- La revisión cruzada no se puede hacer sola: **consultá a los supervisores** si aceptan que un compañero, un docente o un conocido técnico revise algunos PR (basta con que comente y apruebe), o cómo evaluarán ese punto en un proyecto individual.
- Hacé commits chicos y seguidos desde la primera semana; el historial es tu prueba de constancia.
- Escribí el tablero con tarjetas granulares (una por tarea técnica) y mantenelo al día.
