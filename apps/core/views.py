from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils import timezone

from apps.catalog.models import Producto
from apps.inventory.models import Lote


@login_required
def dashboard(request):
    hoy = timezone.localdate()
    limite = hoy + timedelta(days=30)

    productos = Producto.objects.filter(activo=True)

    lotes = Lote.objects.filter(
        activo=True,
        cantidad_disponible__gt=0,
    )

    stock_total = lotes.aggregate(
        total=Coalesce(Sum("cantidad_disponible"), 0)
    )["total"]

    productos_stock_bajo = 0
    productos_sin_stock = 0

    for producto in productos:
        stock = Lote.objects.filter(
            producto=producto,
            activo=True,
        ).aggregate(
            total=Coalesce(Sum("cantidad_disponible"), 0)
        )["total"]

        if stock == 0:
            productos_sin_stock += 1
        elif stock <= producto.stock_minimo:
            productos_stock_bajo += 1

    lotes_vencidos = lotes.filter(
        fecha_vencimiento__lt=hoy,
    )

    lotes_proximos = lotes.filter(
        fecha_vencimiento__gte=hoy,
        fecha_vencimiento__lte=limite,
    )

    context = {
        "total_productos": productos.count(),
        "stock_total": stock_total,
        "productos_stock_bajo": productos_stock_bajo,
        "productos_sin_stock": productos_sin_stock,
        "total_vencidos": lotes_vencidos.count(),
        "total_proximos": lotes_proximos.count(),
        "lotes_vencidos": lotes_vencidos,
        "lotes_proximos": lotes_proximos,
    }

    return render(request, "core/dashboard.html", context)