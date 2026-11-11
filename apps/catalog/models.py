from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos"
    )
    precio_venta = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    stock_minimo = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        indexes = [models.Index(fields=["nombre"])]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"