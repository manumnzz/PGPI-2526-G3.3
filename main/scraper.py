import requests
from bs4 import BeautifulSoup
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from main.models import Product
import os
import tempfile



BASE_URL = "https://www.hl-tienda-online.com"
ALL_PRODUCTS_URL = f"{BASE_URL}/collections/all"

def download_image(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    # Crear archivo temporal compatible con Py3.12
    img_temp = tempfile.NamedTemporaryFile(delete=False)
    img_temp.write(response.content)
    img_temp.flush()

    return img_temp



def scrape_products():
    productos_scrapeados = []

    html = requests.get(ALL_PRODUCTS_URL).text
    soup = BeautifulSoup(html, "html.parser")

    items = soup.select(".product-card") or soup.select(".grid-product")

    for item in items:
        link = item.select_one("a")
        if not link:
            continue

        product_url = BASE_URL + link["href"]

        # Imagen
        img = item.select_one("img")
        img_url = img["src"] if img else None
        if img_url and img_url.startswith("//"):
            img_url = "https:" + img_url

        # Nombre
        name_el = item.select_one(".product-card__title") or item.select_one(".grid-product__title")
        name = name_el.get_text(strip=True) if name_el else "Producto sin nombre"

        # Precio
        price_el = item.select_one(".product-card__price") or item.select_one(".grid-product__price")
        price_text = price_el.get_text(strip=True).replace("€","").replace(",",".") if price_el else "0"

        try:
            price = float(price_text)
        except:
            price = 0.0

        # Obtener o crear producto
        product, created = Product.objects.get_or_create(
            name=name,
            defaults={
                "price": price,
                "url": product_url,
            }
        )

        if not created:
            product.price = price
            product.url = product_url
            product.save()


        # Descargar imagen
        if img_url:
            print(f"Descargando imagen de: {img_url}")
            img_temp = download_image(img_url)
            product.image.save(os.path.basename(img_url), File(img_temp), save=True)

        product.save()
        productos_scrapeados.append(product)

    return productos_scrapeados
