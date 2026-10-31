from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .models import Lote, MovimientoStock, Descarte


@transaction.atomic
def registrar_movimiento(lote_id, tipo, cantidad, motivo, usuario):
    if tipo not in MovimientoStock.Tipo.values:
        raise ValidationError("El tipo de movimiento no es válido.")

    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
        raise ValidationError("La cantidad debe ser un número entero mayor a cero.")

    if not motivo or not motivo.strip():
        raise ValidationError("Debés indicar el motivo del movimiento.")

    if not usuario or not usuario.is_authenticated:
        raise ValidationError("El movimiento debe tener un usuario válido.")

    lote = Lote.objects.select_for_update().get(pk=lote_id)

    if not lote.activo:
        raise ValidationError("No se pueden registrar movimientos en un lote inactivo.")

    if tipo == MovimientoStock.Tipo.ENTRADA:
        lote.cantidad_disponible = F("cantidad_disponible") + cantidad

    elif tipo == MovimientoStock.Tipo.SALIDA:
        if lote.cantidad_disponible < cantidad:
            raise ValidationError(
                "No hay suficiente stock disponible para realizar la salida."
            )

        lote.cantidad_disponible = F("cantidad_disponible") - cantidad

    lote.save(update_fields=["cantidad_disponible"])

    movimiento = MovimientoStock.objects.create(
        lote=lote,
        tipo=tipo,
        cantidad=cantidad,
        motivo=motivo.strip(),
        usuario=usuario,
    )

    return movimiento


@transaction.atomic
def descartar_lote(lote_id, motivo, usuario):
    if not motivo or not isinstance(motivo, str) or not motivo.strip():
        raise ValidationError("Debés indicar el motivo del descarte.")

    if not usuario or not usuario.is_authenticated:
        raise ValidationError("El descarte debe tener un usuario válido.")

    lote = Lote.objects.select_for_update().get(pk=lote_id)

    if not lote.activo:
        raise ValidationError("Este lote ya se encuentra inactivo.")

    if Descarte.objects.filter(lote=lote, revertido=False).exists():
        raise ValidationError("Este lote ya tiene un descarte sin revertir.")

    cantidad_descartada = lote.cantidad_disponible

    if cantidad_descartada <= 0:
        raise ValidationError("No se puede descartar un lote sin stock disponible.")

    descarte = Descarte.objects.create(
        lote=lote,
        cantidad=cantidad_descartada,
        motivo=motivo.strip(),
        usuario=usuario,
    )

    lote.cantidad_disponible = 0
    lote.activo = False
    lote.save(update_fields=["cantidad_disponible", "activo"])

    return descarte


@transaction.atomic
def revertir_descarte(descarte_id, usuario):
    if not usuario or not usuario.is_authenticated:
        raise ValidationError("La reversión debe tener un usuario válido.")

    descarte = Descarte.objects.select_for_update().get(pk=descarte_id)

    if descarte.revertido:
        raise ValidationError("Este descarte ya fue revertido.")

    lote = Lote.objects.select_for_update().get(pk=descarte.lote_id)

    if lote.activo:
        raise ValidationError("El lote ya se encuentra activo.")

    if lote.fecha_vencimiento < timezone.localdate():
        raise ValidationError("No se puede recuperar un lote vencido.")

    if lote.cantidad_disponible != 0:
        raise ValidationError(
            "El lote tiene una cantidad de stock inesperada."
        )

    lote.cantidad_disponible = descarte.cantidad
    lote.activo = True
    lote.save(update_fields=["cantidad_disponible", "activo"])

    descarte.revertido = True
    descarte.fecha_reversion = timezone.now()
    descarte.usuario_reversion = usuario
    descarte.save(
        update_fields=[
            "revertido",
            "fecha_reversion",
            "usuario_reversion",
        ]
    )

    return descarte