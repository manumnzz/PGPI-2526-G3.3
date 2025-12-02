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
	list_display = ("user", "service", "tarifa", "date", "time", "estado")
	list_filter = ("estado", "service")
	search_fields = ("user__username",)


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ("username", "first_name", "last_name", "mail")
	search_fields = ("username", "mail", "first_name", "last_name")
