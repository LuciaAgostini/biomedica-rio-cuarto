from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from .models import Lote


@login_required
def lote_list(request):
    hoy = timezone.localdate()
    limite = hoy + timedelta(days=30)

    lotes = Lote.objects.filter(
        activo=True
    ).select_related(
        "producto",
        "proveedor"
    ).order_by("fecha_vencimiento")

    for lote in lotes:
        if lote.fecha_vencimiento < hoy:
            lote.estado = "Vencido"
        elif lote.fecha_vencimiento <= limite:
            lote.estado = "Próximo a vencer"
        else:
            lote.estado = "Vigente"

    return render(
        request,
        "inventory/lote_list.html",
        {"lotes": lotes}
    )