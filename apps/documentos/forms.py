from decimal import Decimal

from django import forms
from django.forms import formset_factory

from apps.catalog.models import Producto

from .models import Documento, Vendedor


class DocumentoForm(forms.Form):
    vendedor = forms.ModelChoiceField(
        queryset=Vendedor.objects.filter(activo=True),
        label="Vendedor",
        empty_label="Seleccionar vendedor",
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )

    tipo = forms.ChoiceField(
        choices=Documento.Tipo.choices,
        label="Tipo de documento",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    cliente_nombre = forms.CharField(
        max_length=150,
        label="Nombre del cliente",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nombre o razón social",
            }
        ),
    )

    cliente_cuil = forms.CharField(
        max_length=20,
        required=False,
        label="CUIL del cliente",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "XX-XXXXXXXX-X",
            }
        ),
    )

    cliente_localidad = forms.CharField(
        max_length=150,
        label="Localidad",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Localidad del cliente",
            }
        ),
    )

    tipo_iva = forms.ChoiceField(
        choices=Documento.TipoIVA.choices,
        label="IVA",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    porcentaje_iva = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        initial=Decimal("21.00"),
        min_value=Decimal("0.00"),
        max_value=Decimal("100.00"),
        label="Porcentaje de IVA",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.01",
            }
        ),
    )


class ItemDocumentoForm(forms.Form):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.none(),
        label="Producto",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    cantidad = forms.IntegerField(
        min_value=1,
        label="Cantidad",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "1",
            }
        ),
    )

    precio_unitario = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        label="Precio unitario",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["producto"].queryset = Producto.objects.filter(
            activo=True
        ).order_by("nombre")


ItemDocumentoFormSet = formset_factory(
    ItemDocumentoForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
    max_num=100,
    validate_max=True,
)