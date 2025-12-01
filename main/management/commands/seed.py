from django.core.management.base import BaseCommand
from main.models import Service, Tarifa

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
                """El cuerpo es un sistema en constante ajuste...""",
                "services/Masaje_y_Osteopatía.png",
            ),
            (
                "Par Biomagnético",
                "Equilibra tu energía y fortalece tu bienestar",
                """Nuestro organismo está lleno de campos energéticos...""",
                "services/Par_Biomagnético.png",
            ),
            (
                "Técnicas Emocionales",
                "Libera emociones atrapadas y recupera tu bienestar",
                """Las emociones no solo afectan nuestra mente...""",
                "services/Técnicas_Emocionales.png",
            ),
            (
                "Asesoramiento Nutricional y Estilo de Vida",
                "Aliméntate mejor, siéntete mejor",
                """La alimentación es la base de nuestra energía...""",
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
