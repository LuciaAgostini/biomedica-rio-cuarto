from django.db import models


class Proveedor(models.Model):
    razon_social = models.CharField(max_length=150)
    cuit = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["razon_social"]
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"        
    def __str__(self):
        return f"{self.razon_social} - {self.cuit}"