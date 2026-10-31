from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["codigo", "nombre", "descripcion", "categoria", "stock_minimo"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 3})}

    def clean_codigo(self):
        return self.cleaned_data["codigo"].strip().upper()
