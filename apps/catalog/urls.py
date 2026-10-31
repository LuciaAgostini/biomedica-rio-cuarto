from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.ProductoListView.as_view(), name="producto_list"),
    path("nuevo/", views.ProductoCreateView.as_view(), name="producto_create"),
    path("<int:pk>/editar/", views.ProductoUpdateView.as_view(), name="producto_update"),
    path("<int:pk>/baja/", views.ProductoDeactivateView.as_view(), name="producto_deactivate"),
]
