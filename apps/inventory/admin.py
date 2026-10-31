from datetime import timedelta

from django import forms
from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils import timezone
from django.utils.html import format_html

from .models import Lote, MovimientoStock, Descarte
from .services import (
    registrar_movimiento,
    descartar_lote,
    revertir_descarte,
)


class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ("lote", "tipo", "cantidad", "motivo")

    def clean(self):
        cleaned_data = super().clean()

        lote = cleaned_data.get("lote")
        tipo = cleaned_data.get("tipo")
        cantidad = cleaned_data.get("cantidad")

        if lote and not lote.activo:
            raise ValidationError(
                "No se pueden registrar movimientos en un lote inactivo."
            )

        if lote and tipo == MovimientoStock.Tipo.SALIDA and cantidad:
            if cantidad > lote.cantidad_disponible:
                raise ValidationError(
                    "No hay suficiente stock disponible para realizar la salida."
                )

        return cleaned_data


class DescartarLoteForm(forms.Form):
    motivo = forms.CharField(
        label="Motivo del descarte",
        max_length=200,
        widget=forms.Textarea(attrs={"rows": 3}),
    )


class EstadoVencimientoFilter(admin.SimpleListFilter):
    title = "Estado de vencimiento"
    parameter_name = "estado_vencimiento"

    def lookups(self, request, model_admin):
        return (
            ("vencidos", "Vencidos"),
            ("proximos", "Próximos a vencer (30 días)"),
            ("vigentes", "Vigentes"),
        )

    def queryset(self, request, queryset):
        hoy = timezone.localdate()
        limite = hoy + timedelta(days=30)

        if self.value() == "vencidos":
            return queryset.filter(
                activo=True,
                cantidad_disponible__gt=0,
                fecha_vencimiento__lt=hoy,
            )

        if self.value() == "proximos":
            return queryset.filter(
                activo=True,
                cantidad_disponible__gt=0,
                fecha_vencimiento__gte=hoy,
                fecha_vencimiento__lte=limite,
            )

        if self.value() == "vigentes":
            return queryset.filter(
                activo=True,
                cantidad_disponible__gt=0,
                fecha_vencimiento__gt=limite,
            )

        return queryset


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = (
        "producto",
        "numero_lote",
        "proveedor",
        "fecha_vencimiento",
        "estado_vencimiento",
        "cantidad_disponible",
        "activo",
    )

    search_fields = ("producto__nombre", "numero_lote")
    list_filter = (EstadoVencimientoFilter, "fecha_vencimiento")
    readonly_fields = ("cantidad_disponible",)
    actions = ["descartar_lotes"]

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).filter(activo=True)

    @admin.display(description="Estado de vencimiento")
    def estado_vencimiento(self, obj):
        hoy = timezone.localdate()
        dias_restantes = (obj.fecha_vencimiento - hoy).days

        if dias_restantes < 0:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">● Vencido</span>'
            )

        if dias_restantes <= 30:
            return format_html(
                '<span style="color: #e0a800; font-weight: bold;">● Próximo a vencer ({} días)</span>',
                dias_restantes,
            )

        return format_html(
            '<span style="color: #28a745; font-weight: bold;">● Vigente</span>'
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.cantidad_disponible = 0

        super().save_model(request, obj, form, change)

    @admin.action(description="Descartar lote seleccionado")
    def descartar_lotes(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                "Debés seleccionar un solo lote para descartar.",
                level=messages.ERROR,
            )
            return

        lote = queryset.first()

        if request.POST.get("confirmar_descarte") == "1":
            form = DescartarLoteForm(request.POST)

            if form.is_valid():
                try:
                    descartar_lote(
                        lote_id=lote.pk,
                        motivo=form.cleaned_data["motivo"],
                        usuario=request.user,
                    )

                    self.message_user(
                        request,
                        "El lote se descartó correctamente.",
                        level=messages.SUCCESS,
                    )
                    return None

                except ValidationError as error:
                    form.add_error(None, error)

        else:
            form = DescartarLoteForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "Confirmar descarte de lote",
            "lote": lote,
            "form": form,
            "action_checkbox_name": ACTION_CHECKBOX_NAME,
            "opts": self.model._meta,
        }

        return render(
            request,
            "admin/inventory/confirmar_descarte.html",
            context,
        )


@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    form = MovimientoStockForm

    list_display = (
        "lote",
        "tipo",
        "cantidad",
        "motivo",
        "usuario",
        "fecha",
    )

    search_fields = ("lote__numero_lote", "motivo")
    list_filter = ("tipo", "fecha")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return (
                "lote",
                "tipo",
                "cantidad",
                "motivo",
                "usuario",
                "fecha",
            )

        return ()

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False

        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        movimiento = registrar_movimiento(
            lote_id=obj.lote_id,
            tipo=obj.tipo,
            cantidad=obj.cantidad,
            motivo=obj.motivo,
            usuario=request.user,
        )

        obj.pk = movimiento.pk
        obj.usuario = movimiento.usuario
        obj.fecha = movimiento.fecha
        obj._state.adding = False


@admin.register(Descarte)
class DescarteAdmin(admin.ModelAdmin):
    list_display = (
        "producto",
        "numero_lote",
        "cantidad",
        "motivo",
        "estado_descarte",
        "usuario",
        "fecha",
        "usuario_reversion",
        "fecha_reversion",
    )

    search_fields = (
        "lote__producto__nombre",
        "lote__numero_lote",
        "motivo",
    )

    list_filter = ("revertido", "fecha")

    readonly_fields = (
        "lote",
        "cantidad",
        "motivo",
        "usuario",
        "fecha",
        "revertido",
        "usuario_reversion",
        "fecha_reversion",
    )

    actions = ["revertir_descartes"]

    @admin.display(description="Producto")
    def producto(self, obj):
        return obj.lote.producto.nombre

    @admin.display(description="Número de lote")
    def numero_lote(self, obj):
        return obj.lote.numero_lote

    @admin.display(description="Estado")
    def estado_descarte(self, obj):
        if obj.revertido:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">● Revertido</span>'
            )

        return format_html(
            '<span style="color: #dc3545; font-weight: bold;">● Descartado</span>'
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description="Revertir descarte seleccionado")
    def revertir_descartes(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                "Debés seleccionar un solo descarte para revertir.",
                level=messages.ERROR,
            )
            return

        descarte = queryset.first()

        if descarte.revertido:
            self.message_user(
                request,
                "Este descarte ya fue revertido.",
                level=messages.ERROR,
            )
            return

        if request.POST.get("confirmar_reversion") == "1":
            try:
                revertir_descarte(
                    descarte_id=descarte.pk,
                    usuario=request.user,
                )

                self.message_user(
                    request,
                    "El descarte se revirtió correctamente. "
                    "El lote volvió al inventario.",
                    level=messages.SUCCESS,
                )
                return None

            except ValidationError as error:
                self.message_user(
                    request,
                    "; ".join(error.messages),
                    level=messages.ERROR,
                )
                return None

        context = {
            **self.admin_site.each_context(request),
            "title": "Confirmar reversión de descarte",
            "descarte": descarte,
            "action_checkbox_name": ACTION_CHECKBOX_NAME,
            "opts": self.model._meta,
        }

        return render(
            request,
            "admin/inventory/confirmar_reversion.html",
            context,
        )