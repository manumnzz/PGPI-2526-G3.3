from django.db import models
from django.contrib.auth.models import User as DjangoUser

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField(max_length=200)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.name} - ${self.price}"
    
class Service(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    imagen_der = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class User(models.Model):
    # Perfil asociado al usuario de Django
    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name="profile")

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    mail = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    telephone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"
    
class Tarifa(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="tarifas")
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.service.title} - {self.title} ({self.price}€)"

class Cita(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="citas")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    estado = models.CharField(
        max_length=20,
        choices=[
            ("activa", "Activa"),
            ("cancelada", "Cancelada"),
            ("modificada", "Modificada"),
        ],
        default="activa"
    )

    def __str__(self):
        return f"{self.user.username} - {self.service.title} ({self.date} {self.time})"
