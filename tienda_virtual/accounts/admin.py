from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Información adicional",
            {
                "fields": (
                    "direccion",
                    "codigo_postal",
                    "fecha_nacimiento",
                    "telefono",
                    "rol",
                )
            },
        ),
    )
    list_display = ("username", "email", "rol", "is_staff", "is_active")
