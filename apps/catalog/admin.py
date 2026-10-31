from django.contrib import admin
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from django.utils.html import format_html

from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa")
    search_fields = ("nombre",)
    list_filter = ("activa",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "categoria",
        "stock_total",
        "stock_minimo",
        "estado_stock",
        "activo",
    )

    search_fields = ("codigo", "nombre")
    list_filter = ("categoria", "activo")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.annotate(
            total_stock=Coalesce(
                Sum(
                    "lotes__cantidad_disponible",
                    filter=Q(lotes__activo=True),
                ),
                0,
            )
        )

    @admin.display(description="Stock disponible", ordering="total_stock")
    def stock_total(self, obj):
        return obj.total_stock

    @admin.display(description="Estado del stock")
    def estado_stock(self, obj):
        stock = obj.total_stock
        minimo = obj.stock_minimo

        if stock == 0:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">● Sin stock</span>'
            )

        if stock < minimo:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">● Stock bajo</span>'
            )

        if stock == minimo:
            return format_html(
                '<span style="color: #e0a800; font-weight: bold;">● Stock mínimo</span>'
            )

        return format_html(
            '<span style="color: #28a745; font-weight: bold;">● Normal</span>'
        )