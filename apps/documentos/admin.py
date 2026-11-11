from django.contrib import admin

from .models import Vendedor


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "razon_social",
        "cuit",
        "telefono",
        "email",
        "activo",
    )

    list_filter = ("activo",)

    search_fields = (
        "nombre",
        "razon_social",
        "cuit",
    )

    list_editable = ("activo",)