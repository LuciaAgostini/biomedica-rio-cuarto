from django import forms

from .models import Proveedor


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["razon_social", "cuit", "telefono", "email"]

    def clean_cuit(self):
        cuit = self.cleaned_data["cuit"].strip()

        if not cuit:
            raise forms.ValidationError("El CUIT es obligatorio.")

        return cuit