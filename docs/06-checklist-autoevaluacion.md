# Checklist contra los criterios de evaluación (punto 5)

## 1. Rigor metodológico y trabajo colaborativo
- [ ] Tablero Kanban con tarjetas asignadas y estados al día
- [ ] Cada PR enlaza su tarjeta
- [ ] Commits regulares durante todo el período (no solo al final)
- [ ] Ningún commit directo a `main`
- [ ] Todos los PR con descripción y, si es posible, revisión de otra persona (consultar a los supervisores)
- [ ] Evidencia de trabajo en backend, frontend, base de datos y tests

## 2. Arquitectura y código
- [ ] Lógica de negocio en `services.py`, no en vistas ni templates
- [ ] Sin código duplicado; funciones cortas y con nombres claros
- [ ] `ruff check .` sin errores

## 3. Funcionalidad
- [ ] MVP completo: login, roles, 3+ CRUDs vinculados (Producto, Proveedor, Lote) con baja lógica
- [ ] Validaciones en frontend y backend
- [ ] Mensajes de éxito, error y advertencia
- [ ] Pantalla de próximos a vencer funcionando

## 4. Seguridad y persistencia
- [ ] Contraseñas con hash; sesiones seguras; CSRF activo
- [ ] Todas las vistas protegidas por rol
- [ ] Sin secretos en el repo; `.env.example` presente; revisar el historial de Git
- [ ] Migraciones versionadas; claves foráneas e índices

## 5. Testing
- [ ] Tests de RN-01 a RN-14
- [ ] `pytest --cov=apps` con cobertura razonable en reglas de negocio

## 6. Deploy y documentación
- [ ] App funcionando en la nube con HTTPS
- [ ] README completo y reproducible
- [ ] Swagger en `/api/docs/` con todos los endpoints
- [ ] Usuarios de prueba (Administrador y Superadministrador) documentados para los docentes
