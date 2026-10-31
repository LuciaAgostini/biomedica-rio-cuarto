<p align="center"><img src="static/img/logo-principal.png" alt="Biomédica Río Cuarto" width="320"></p>

# Biomédica Río Cuarto · Gestión de stock y vencimientos

Sistema web para una distribuidora de insumos de laboratorio e insumos médicos de Río Cuarto. Controla productos, proveedores, lotes y movimientos de stock, y avisa qué lotes están próximos a vencer.

> Práctica Profesionalizante II · Tecnicatura Superior en Desarrollo de Software · 2026

**Demo en producción:** _(completar URL)_ · **API docs:** `/api/docs/`

## Integrantes
| Nombre | Usuario Git |
|---|---|
| _Integrante 1_ | @ |




## Stack
Python 3.12 · Django 5 · Django REST Framework · PostgreSQL · Bootstrap 5 · drf-spectacular (OpenAPI) · pytest-django · Render/Railway (deploy)

## Arquitectura
Capas dentro de cada app de `apps/`:

```
Presentación   views.py, templates/, serializers.py
Negocio        services.py   (reglas: FEFO, vencimientos, stock)
Datos          models.py + migraciones
```

Apps: `accounts` (usuarios y roles), `catalog` (categorías y productos), `suppliers` (proveedores), `inventory` (lotes, movimientos, vencimientos), `audit` (registro de actividad), `core` (utilidades y permisos).

## Roles
| Rol | Alcance |
|---|---|
| Administrador | Productos, proveedores, lotes, movimientos, stock bajo, próximos a vencer |
| Superadministrador | Todo lo anterior + usuarios/roles, categorías, parámetros, registro de actividad |

## Prerrequisitos
Python 3.12+, PostgreSQL 15+, Git.

## Ejecución local
```bash
git clone <url-del-repo> && cd biomedica
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # completar valores
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Variables de entorno
Ver `.env.example`. Variables: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`, `CSRF_TRUSTED_ORIGINS`, `DJANGO_SETTINGS_MODULE`.

## Tests
```bash
pytest --cov=apps
ruff check .
```

## Deploy
Ver `docs/07-deploy.md`.

## Documentación
- `docs/01-historias-de-usuario.md`
- `docs/02-reglas-de-negocio-y-tests.md`
- `docs/03-modelo-de-datos.md`
- `docs/04-tablero-kanban.md`
- `docs/05-convenciones-git.md`
- `docs/06-checklist-autoevaluacion.md`
