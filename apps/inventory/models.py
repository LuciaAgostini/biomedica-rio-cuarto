from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.catalog.models import Producto
from apps.suppliers.models import Proveedor


class Lote(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="lotes",
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="lotes",
    )
    numero_lote = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField()
    cantidad_disponible = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["fecha_vencimiento"]
        verbose_name = "Lote"
        verbose_name_plural = "Lotes"
        constraints = [
            models.UniqueConstraint(
                fields=["producto", "numero_lote"],
                name="unique_producto_numero_lote",
            ),
            models.CheckConstraint(
                condition=models.Q(cantidad_disponible__gte=0),
                name="lote_cantidad_disponible_gte_0",
            ),
        ]
        indexes = [
            models.Index(fields=["fecha_vencimiento"]),
        ]

    def __str__(self):
        return f"{self.producto.nombre} - Lote {self.numero_lote}"


class MovimientoStock(models.Model):
    class Tipo(models.TextChoices):
        ENTRADA = "ENTRADA", "Entrada"
        SALIDA = "SALIDA", "Salida"

    lote = models.ForeignKey(
        Lote,
        on_delete=models.PROTECT,
        related_name="movimientos",
    )
    tipo = models.CharField(
        max_length=10,
        choices=Tipo.choices,
    )
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    motivo = models.CharField(max_length=200)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="movimientos_stock",
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Movimiento de stock"
        verbose_name_plural = "Movimientos de stock"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad__gt=0),
                name="movimiento_cantidad_gt_0",
            ),
        ]
        indexes = [
            models.Index(fields=["lote", "fecha"]),
        ]

    def __str__(self):
        return f"{self.tipo} - {self.lote.numero_lote} - {self.cantidad}"


class Descarte(models.Model):
    lote = models.ForeignKey(
        Lote,
        on_delete=models.PROTECT,
        related_name="descartes",
    )
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    motivo = models.CharField(max_length=200)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="descartes_realizados",
    )
    fecha = models.DateTimeField(auto_now_add=True)

    revertido = models.BooleanField(default=False)

    fecha_reversion = models.DateTimeField(
        null=True,
        blank=True,
    )

    usuario_reversion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="descartes_revertidos",
    )

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Descarte"
        verbose_name_plural = "Historial de descartados"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad__gt=0),
                name="descarte_cantidad_gt_0",
            ),
            models.UniqueConstraint(
                fields=["lote"],
                condition=models.Q(revertido=False),
                name="unique_descarte_activo_por_lote",
            ),
        ]

    def __str__(self):
        return f"Descarte de {self.lote.numero_lote} - {self.cantidad} unidades"