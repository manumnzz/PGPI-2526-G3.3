from django.core.management.base import BaseCommand
from main.scraper import scrape_products

class Command(BaseCommand):
    help = "Actualiza productos desde HL Tienda Online"

    def handle(self, *args, **options):
        print("⏳ Scraping productos de Herbalife...")

        scraped = scrape_products()

        print(f"🔍 Encontrados {len(scraped)} productos")

        # Mostrar resumen (opcional)
        for p in scraped:
            print(f"✔ {p.name} — €{p.price}")
        
        print("🎉 Actualización completada.")
