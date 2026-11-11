from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Vendedor(models.Model):
    nombre = models.CharField(max_length=150)
    razon_social = models.CharField(max_length=200)
    cuit = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"

    def __str__(self):
        return f"{self.nombre} - {self.razon_social} ({self.cuit})"


class NumeracionDocumento(models.Model):
    tipo = models.CharField(
        max_length=15,
        unique=True,
        choices=[
            ("PRESUPUESTO", "Presupuesto"),
            ("REMITO", "Remito"),
        ],
    )
    ultimo_numero = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.tipo}: {self.ultimo_numero}"


class Documento(models.Model):
    class Tipo(models.TextChoices):
        PRESUPUESTO = "PRESUPUESTO", "Presupuesto"
        REMITO = "REMITO", "Remito"

    class Estado(models.TextChoices):
        BORRADOR = "BORRADOR", "Borrador"
        CONFIRMADO = "CONFIRMADO", "Confirmado"
        ANULADO = "ANULADO", "Anulado"

    class TipoIVA(models.TextChoices):
        SIN_IVA = "SIN_IVA", "Sin IVA"
        INCLUIDO = "INCLUIDO", "IVA incluido"
        DISCRIMINADO = "DISCRIMINADO", "IVA discriminado"

    tipo = models.CharField(
        max_length=15,
        choices=Tipo.choices,
    )

    numero = models.PositiveIntegerField()

    fecha = models.DateField(auto_now_add=True)

    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.PROTECT,
        related_name="documentos",
        null=True,
        blank=True,
    )

    vendedor_nombre = models.CharField(max_length=150)

    vendedor_cuil = models.CharField(max_length=20)

    vendedor_razon_social = models.CharField(max_length=200)

    vendedor_telefono = models.CharField(
        max_length=30,
        blank=True,
        default="",
    )

    vendedor_email = models.EmailField(
        blank=True,
        default="",
    )

    cliente_nombre = models.CharField(max_length=150)

    cliente_cuil = models.CharField(
        max_length=20,
        blank=True,
    )

    cliente_localidad = models.CharField(max_length=150)

    tipo_iva = models.CharField(
        max_length=15,
        choices=TipoIVA.choices,
        default=TipoIVA.SIN_IVA,
    )

    porcentaje_iva = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("21.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )

    estado = models.CharField(
        max_length=15,
        choices=Estado.choices,
        default=Estado.BORRADOR,
    )

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="documentos_creados",
    )

    creado_en = models.DateTimeField(auto_now_add=True)

    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha", "-numero"]
        constraints = [
            models.UniqueConstraint(
                fields=["tipo", "numero"],
                name="documento_tipo_numero_unico",
            )
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} N.º {self.numero:08d}"

    @property
    def numero_formateado(self):
        return f"{self.numero:08d}"

    @property
    def subtotal(self):
        return sum(
            (item.total for item in self.items.all()),
            Decimal("0.00"),
        )

    @property
    def importe_iva(self):
        if self.tipo_iva == self.TipoIVA.SIN_IVA:
            return Decimal("0.00")

        porcentaje = self.porcentaje_iva / Decimal("100")

        if self.tipo_iva == self.TipoIVA.INCLUIDO:
            return (
                self.subtotal
                - self.subtotal / (Decimal("1") + porcentaje)
            ).quantize(Decimal("0.01"))

        return (
            self.subtotal * porcentaje
        ).quantize(Decimal("0.01"))

    @property
    def total(self):
        if self.tipo_iva == self.TipoIVA.DISCRIMINADO:
            return self.subtotal + self.importe_iva

        return self.subtotal


class ItemDocumento(models.Model):
    documento = models.ForeignKey(
        Documento,
        on_delete=models.CASCADE,
        related_name="items",
    )

    producto = models.ForeignKey(
        "catalog.Producto",
        on_delete=models.PROTECT,
        related_name="items_documentos",
    )

    codigo = models.CharField(max_length=30)

    descripcion = models.CharField(max_length=250)

    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )

    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )

    class Meta:
        ordering = ["id"]

    @property
    def total(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.descripcion} - {self.cantidad}"