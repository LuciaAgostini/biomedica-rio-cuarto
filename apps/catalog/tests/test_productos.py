import pytest
from django.urls import reverse

from apps.accounts.models import User
from apps.catalog.models import Categoria, Producto


@pytest.fixture
def categoria(db):
    return Categoria.objects.create(nombre="Descartables")


@pytest.fixture
def admin_client(client, db):
    user = User.objects.create_user("dueno", password="Clave-segura-123", role=User.Role.ADMIN)
    client.force_login(user)
    return client


def test_listado_requiere_login(client, db):
    resp = client.get(reverse("catalog:producto_list"))
    assert resp.status_code == 302


def test_crear_producto_normaliza_codigo(admin_client, categoria):
    resp = admin_client.post(
        reverse("catalog:producto_create"),
        {"codigo": " gua-01 ", "nombre": "Guantes de látex", "categoria": categoria.pk, "stock_minimo": 10},
    )
    assert resp.status_code == 302
    assert Producto.objects.get().codigo == "GUA-01"


def test_baja_es_logica(admin_client, categoria):
    p = Producto.objects.create(codigo="X1", nombre="Gasas", categoria=categoria)
    admin_client.post(reverse("catalog:producto_deactivate", args=[p.pk]))
    p.refresh_from_db()
    assert p.activo is False
    assert Producto.objects.filter(pk=p.pk).exists()
