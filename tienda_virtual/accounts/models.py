from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        CLIENTE = "CLIENTE", "Cliente"

    direccion = models.CharField(max_length=255, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    rol = models.CharField(
        max_length=20, choices=Roles.choices, default=Roles.CLIENTE
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.get_rol_display()})"
