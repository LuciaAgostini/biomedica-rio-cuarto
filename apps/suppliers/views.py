from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, UpdateView

from .forms import ProveedorForm
from .models import Proveedor


class ProveedorListView(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = "suppliers/lista_proveedores.html"
    context_object_name = "proveedores"
    paginate_by = 10

    def get_queryset(self):
        proveedores = Proveedor.objects.all()

        busqueda = self.request.GET.get("q", "").strip()
        estado = self.request.GET.get("estado", "todos")

        if busqueda:
            proveedores = proveedores.filter(
                Q(razon_social__icontains=busqueda) |
                Q(cuit__icontains=busqueda)
            )

        if estado == "activos":
            proveedores = proveedores.filter(activo=True)
        elif estado == "inactivos":
            proveedores = proveedores.filter(activo=False)

        return proveedores.order_by("razon_social")

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["busqueda"] = self.request.GET.get("q", "").strip()
        contexto["estado"] = self.request.GET.get("estado", "todos")
        return contexto


class ProveedorCreateView(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "suppliers/form_proveedor.html"
    success_url = reverse_lazy("suppliers:lista")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Proveedor creado correctamente."
        )
        return super().form_valid(form)


class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "suppliers/form_proveedor.html"
    success_url = reverse_lazy("suppliers:lista")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Proveedor actualizado correctamente."
        )
        return super().form_valid(form)


@login_required
@require_POST
def inactivar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)

    proveedor.activo = False
    proveedor.save(update_fields=["activo"])

    messages.warning(
        request,
        "Proveedor inactivado correctamente."
    )

    return redirect("suppliers:lista")


@login_required
@require_POST
def activar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)

    proveedor.activo = True
    proveedor.save(update_fields=["activo"])

    messages.success(
        request,
        "Proveedor activado correctamente."
    )

    return redirect("suppliers:lista")