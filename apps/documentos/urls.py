from django.urls import path

from . import views

app_name = "documentos"

urlpatterns = [
    path("", views.documento_list, name="documento_list"),
    path("nuevo/", views.documento_crear, name="documento_crear"),

    path(
        "presupuestos/",
        views.documento_list,
        {"tipo_documento": "PRESUPUESTO"},
        name="presupuesto_list",
    ),
    path(
        "presupuestos/nuevo/",
        views.documento_crear,
        {"tipo_documento": "PRESUPUESTO"},
        name="presupuesto_crear",
    ),

    path(
        "remitos/",
        views.documento_list,
        {"tipo_documento": "REMITO"},
        name="remito_list",
    ),
    path(
        "remitos/nuevo/",
        views.documento_crear,
        {"tipo_documento": "REMITO"},
        name="remito_crear",
    ),

    path("<int:pk>/pdf/", views.documento_pdf, name="documento_pdf"),
]