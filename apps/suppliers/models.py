from django.db import models


class Proveedor(models.Model):
    razon_social = models.CharField(max_length=150)
    cuit = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    localidad = models.CharField(max_length=100, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    persona_contacto = models.CharField(max_length=150, blank=True)
    observaciones = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["razon_social"]
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return f"{self.razon_social} - {self.cuit}"