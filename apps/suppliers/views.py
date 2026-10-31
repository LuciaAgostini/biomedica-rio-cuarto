from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import ProveedorForm
from .models import Proveedor


class ProveedorListView(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = "suppliers/lista_proveedores.html"
    context_object_name = "proveedores"

    def get_queryset(self):
        return Proveedor.objects.filter(activo=True)


class ProveedorCreateView(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "suppliers/form_proveedor.html"
    success_url = reverse_lazy("suppliers:lista")

    def form_valid(self, form):
        messages.success(self.request, "Proveedor creado correctamente.")
        return super().form_valid(form)


class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "suppliers/form_proveedor.html"
    success_url = reverse_lazy("suppliers:lista")

    def form_valid(self, form):
        messages.success(self.request, "Proveedor actualizado correctamente.")
        return super().form_valid(form)


def inactivar_proveedor(request, pk):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    proveedor = Proveedor.objects.get(pk=pk)
    proveedor.activo = False
    proveedor.save(update_fields=["activo"])

    messages.warning(request, "Proveedor inactivado correctamente.")
    return redirect("suppliers:lista")