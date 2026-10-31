from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from apps.core.permissions import RoleRequiredMixin

from .forms import ProductoForm
from .models import Producto


class ProductoListView(RoleRequiredMixin, ListView):
    model = Producto
    template_name = "catalog/producto_list.html"
    paginate_by = 20

    def get_queryset(self):
        qs = Producto.objects.filter(activo=True).select_related("categoria")
        q = self.request.GET.get("q")
        return qs.filter(nombre__icontains=q) if q else qs


class ProductoCreateView(RoleRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "catalog/producto_form.html"
    success_url = reverse_lazy("catalog:producto_list")

    def form_valid(self, form):
        messages.success(self.request, "Producto creado correctamente.")
        return super().form_valid(form)


class ProductoUpdateView(RoleRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "catalog/producto_form.html"
    success_url = reverse_lazy("catalog:producto_list")

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado correctamente.")
        return super().form_valid(form)


class ProductoDeactivateView(RoleRequiredMixin, View):
    """Baja lógica: solo por POST."""

    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk, activo=True)
        producto.activo = False
        producto.save(update_fields=["activo"])
        messages.warning(request, f"Producto «{producto.nombre}» dado de baja.")
        return redirect("catalog:producto_list")
