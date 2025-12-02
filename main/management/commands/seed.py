from django.core.management.base import BaseCommand
from django.contrib.auth.models import User as DjangoUser
from main.models import Service, Tarifa, User

class Command(BaseCommand):
    help = "Seed database with initial Natursur data"

    def handle(self, *args, **kwargs):
        print("⏳ Seeding database...")
        self.create_services()
        self.create_tarifas()
        print("🎉 Seed completed successfully!")

    # -------------------------------------------------
    # SERVICES
    # -------------------------------------------------
    def create_services(self):

        services = [
            (
                "Masaje y Osteopatía",
                "Restablece el equilibrio de tu cuerpo",
                """El cuerpo es un sistema en constante ajuste. El dolor, la tensión o la falta de movilidad son señales de que algo no está funcionando bien. A través de técnicas de masaje y osteopatía, trabajamos para liberar restricciones, mejorar la postura y restaurar la armonía de tu organismo. Mi objetivo es ayudarte a moverte sin dolor y con mayor libertad, respetando siempre la estructura natural de tu cuerpo.""",
                "services/Masaje_y_Osteopatía.png",
            ),
            (
                "Par Biomagnético",
                "Equilibra tu energía y fortalece tu bienestar",
                """Nuestro organismo está lleno de campos energéticos que, en ocasiones, se ven alterados por virus, bacterias o desequilibrios internos. El Par Biomagnético es una técnica que utiliza imanes para restaurar el balance natural del cuerpo, favoreciendo la capacidad de recuperación del organismo. Si buscas una terapia complementaria para mejorar tu bienestar, esta puede ser una excelente opción.""",
                "services/Par_Biomagnético.png",
            ),
            (
                "Técnicas Emocionales",
                "Libera emociones atrapadas y recupera tu bienestar",
                """Las emociones no solo afectan nuestra mente, también pueden dejar huella en nuestro cuerpo. Muchas tensiones musculares, bloqueos o molestias físicas tienen un origen emocional. Utilizo diversas técnicas para ayudarte a liberar esas cargas y sentirte más ligero y equilibrado.

Referencia: "El Código de la Emoción"
«Este libro de Dr. Bradley Nelson explica cómo las emociones pueden quedarse atrapadas en nuestro cuerpo y afectar nuestro bienestar. Basándome en estos principios, aplico técnicas para identificar y liberar esas emociones acumuladas.»""",
                "services/Técnicas_Emocionales.png",
            ),
            (
                "Asesoramiento Nutricional y Estilo de Vida",
                "Aliméntate mejor, siéntete mejor",
                """La alimentación es la base de nuestra energía y bienestar. No se trata solo de perder peso,
sino de aprender a nutrir el cuerpo de forma adecuada. A través de un enfoque basado en la naturopatía, te ayudo a mejorar tu alimentación y a crear hábitos saludables que realmente funcionen para ti.""",
                "services/Asesoramiento_Nutricional_y_Estilo_de_Vida.png",
            ),
        ]

        for title, subtitle, description, img_path in services:

            if Service.objects.filter(title=title).exists():
                continue

            Service.objects.create(
                title=title,
                subtitle=subtitle,
                description=description,
                imagen_der=True,
                image=img_path  # <<< ruta a static
            )

        print("✔ Servicios creados")

    # -------------------------------------------------
    # TARIFAS
    # -------------------------------------------------
    def create_tarifas(self):

        tarifas = [
            ("Sesión 40´", 28, ""),
            ("Sesión 60´", 45, ""),
            ("Sesión 90´", 70, ""),
            ("3 sesiones de 40´", 70, ""),
            ("Sesión Premium 60´", 50, "Masaje, osteopatía, par biomagnético y emociones atrapadas."),
            ("Domicilio 60´", 100, ""),
        ]

        servicio_base = Service.objects.first()
        if not servicio_base:
            print("⚠ No hay servicios creados aún.")
            return

        for title, price, description in tarifas:
            if Tarifa.objects.filter(title=title, service=servicio_base).exists():
                continue

            Tarifa.objects.create(
                service=servicio_base,
                title=title,
                price=price,
                description=description
            )

        print("✔ Tarifas creadas")

    def create_test_user(self):

        if DjangoUser.objects.filter(username="user1").exists():
            print("✔ Usuario de prueba ya existe")
            return

        django_user = DjangoUser.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="user123" 
        )

        User.objects.create(
            django_user=django_user,
            first_name="user",
            last_name="1",
            username="user1",
            mail="user1@example.com",
            direccion="Calle Ejemplo 123",
            postal_code="41001",
            age=25,
            telephone_number="600123123",
            password=django_user.password 
        )

        print("✔ Usuario de prueba creado")
