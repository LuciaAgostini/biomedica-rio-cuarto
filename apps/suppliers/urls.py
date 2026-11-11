from django.urls import path

from .views import (
    ProveedorCreateView,
    ProveedorListView,
    ProveedorUpdateView,
    activar_proveedor,
    inactivar_proveedor,
)

app_name = "suppliers"

urlpatterns = [
    path("", ProveedorListView.as_view(), name="lista"),
    path("crear/", ProveedorCreateView.as_view(), name="crear"),
    path("editar/<int:pk>/", ProveedorUpdateView.as_view(), name="editar"),
    path("inactivar/<int:pk>/", inactivar_proveedor, name="inactivar"),
    path("activar/<int:pk>/", activar_proveedor, name="activar"),
]