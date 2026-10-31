# Deploy (Render, con PostgreSQL)

1. Crear una base **PostgreSQL** en Render y copiar su `Internal Database URL`.
2. Crear un **Web Service** conectado al repo.
   - Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start: `gunicorn config.wsgi:application`
3. Variables de entorno: `DJANGO_SETTINGS_MODULE=config.settings.prod`, `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=<tu-app>.onrender.com`, `CSRF_TRUSTED_ORIGINS=https://<tu-app>.onrender.com`, `DATABASE_URL`.
4. Crear el Superadministrador desde la consola de Render: `python manage.py createsuperuser`, y luego asignar `role=SUPERADMIN` desde el admin de Django.
5. Verificar `/login/` y `/api/docs/`.
