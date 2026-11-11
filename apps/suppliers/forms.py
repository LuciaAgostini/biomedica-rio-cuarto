from django import forms

from .models import Proveedor


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            "razon_social",
            "cuit",
            "telefono",
            "email",
            "direccion",
            "localidad",
            "provincia",
            "persona_contacto",
            "observaciones",
            "activo",
        ]

        labels = {
            "razon_social": "Razón social",
            "cuit": "CUIT",
            "telefono": "Teléfono",
            "email": "Correo electrónico",
            "direccion": "Dirección",
            "localidad": "Localidad",
            "provincia": "Provincia",
            "persona_contacto": "Persona de contacto",
            "observaciones": "Observaciones",
            "activo": "Proveedor activo",
        }

        widgets = {
            "razon_social": forms.TextInput(attrs={"class": "form-control"}),
            "cuit": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "localidad": forms.TextInput(attrs={"class": "form-control"}),
            "provincia": forms.TextInput(attrs={"class": "form-control"}),
            "persona_contacto": forms.TextInput(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_cuit(self):
        cuit = self.cleaned_data["cuit"].strip()

        if not cuit:
            raise forms.ValidationError("El CUIT es obligatorio.")

        return cuit