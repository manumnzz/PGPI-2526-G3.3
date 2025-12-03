
# 🌿 Natursur — Plataforma Web de Bienestar & Tienda Herbalife

Natursur es una plataforma web profesional desarrollada en **Django 5** que integra:

- Gestión completa de usuarios  
- Reserva de citas para servicios de bienestar  
- Catálogo de productos Herbalife con *scraping automático*  
- **Chatbot inteligente** alimentado por IA (Groq Llama 3.3)  
- Interfaz moderna, fluida y adaptada para personas mayores  

Este proyecto está orientado a una consulta real y refleja un sitio profesional y funcional.

---

## ✨ Funcionalidades principales

### 🧑‍💼 Gestión de usuarios
- Registro e inicio de sesión
- Perfil editable con imagen
- Información personal detallada (edad, teléfono, dirección…)
- Sistema completo de cierre de sesión

### 📅 Gestión de citas
- Selección de servicio y tarifa
- Calendario y horarios personalizables
- Crear, editar y cancelar citas
- Las citas se asocian al perfil del usuario

### 🛒 Catálogo de productos Herbalife
- Scraping automático desde el sitio HL tienda online
- Evita duplicados: actualiza precio, imagen y URL solo si cambian
- Búsqueda y filtrado por precio
- Imágenes descargadas y almacenadas en `/images/products/`

### 🤖 Chatbot con IA (Groq)
El asistente es capaz de:

- Entender nombres incorrectos o incompletos ("batido para adelgazar")
- Ofrecer productos probables
- Enviar enlaces clicables
- Guiar al usuario por la web
- Crear citas automáticamente si tiene todos los datos
- Mantener contexto básico ("sí", "correcto", "esa")

Modelo: **llama-3.3-70b-versatile** sobre **Groq API**.

---

## 🛠️ Tecnologías

| Categoría | Tecnologías |
|----------|-------------|
| Backend | Django 5, Python 3.12 |
| IA | Groq API |
| Frontend | Bootstrap 5, HTML5, CSS3 |
| Base de datos | SQLite |
| Scraping | Requests + BeautifulSoup |
| Media | Pillow |
| Env | python-dotenv |

---

# 📦 Instalación

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/manumnzz/PGPI-2526-G3.3.git
cd PGPI-2526-G3.3
```

## 2️⃣ Crear y activar un entorno virtual

```bash
python -m venv venv
```

Activarlo:

- **Windows**
  ```bash
  venv\Scripts\activate
  ```
- **Mac / Linux**
  ```bash
  source venv/bin/activate
  ```

## 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4️⃣ Configurar variables de entorno (.env)

Crea un archivo llamado `.env` en la raíz del proyecto:

```
GROQ_API_KEY=TU_API_KEY_AQUI
GROQ_MODEL=llama-3.3-70b-versatile
```

## 5️⃣ Aplicar migraciones

```bash
python manage.py migrate
```

## 6️⃣ Crear un superusuario

```bash
python manage.py createsuperuser
```

Acceder al panel:

```
http://127.0.0.1:8000/admin/
```

## 7️⃣ (Opcional) Poblar productos mediante scraping

```bash
python manage.py shell
```

Luego:

```python
from main.scraper import scrape_products
scrape_products()
exit()
```

## 8️⃣ Ejecutar el servidor

```bash
python manage.py runserver
```

Ir a:

```
http://127.0.0.1:8000/
```

---

# 🧑‍💻 Autor

**Manuel Buzón Muñoz (manumnzz)**  
**Dario Rodriguez Sastre (darrodsas)**  
**Mario Astudillo Fierro (marastfie)**  
**Fernando Murillo Bravo ()**  
**Manuel Lavado Corredera (60Manu82)**  

Proyecto universitario real para una consulta profesional.

