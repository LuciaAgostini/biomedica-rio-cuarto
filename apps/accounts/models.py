from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        SUPERADMIN = "SUPERADMIN", "Superadministrador"

    role = models.CharField(max_length=12, choices=Role.choices, default=Role.ADMIN)

    @property
    def is_superadmin_role(self) -> bool:
        return self.role == self.Role.SUPERADMIN
