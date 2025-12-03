from django.contrib import admin
from .models import Product, Service, Tarifa, Cita, User


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "imagen_der")
    search_fields = ("title", "subtitle")


@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ("service", "title", "price")
    list_filter = ("service",)


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("get_username", "service", "tarifa", "date", "time", "estado")
    list_filter = ("estado", "service")
    search_fields = ("user__django_user__username",)

    # Mostrar correctamente el username del usuario
    def get_username(self, obj):
        return obj.user.django_user.username
    get_username.short_description = "Usuario"


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("get_username", "get_email", "get_full_name", "age", "telephone_number")
    search_fields = ("django_user__username", "django_user__email", "django_user__first_name", "django_user__last_name")

    # Campos derivados del DjangoUser asociado
    def get_username(self, obj):
        return obj.django_user.username
    get_username.short_description = "Usuario"

    def get_email(self, obj):
        return obj.django_user.email
    get_email.short_description = "Email"

    def get_full_name(self, obj):
        return f"{obj.django_user.first_name} {obj.django_user.last_name}"
    get_full_name.short_description = "Nombre Completo"
