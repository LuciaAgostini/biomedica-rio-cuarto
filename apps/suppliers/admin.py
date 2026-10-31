from django.contrib import admin
from .models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("razon_social", "cuit", "telefono", "email", "activo")
    search_fields = ("razon_social", "cuit")
    list_filter = ("activo",)