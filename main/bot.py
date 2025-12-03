import os
import json
import requests

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

from .models import Product, Service, Tarifa, Cita

CONFIRMATIONS = [
    "sí", "si", "correcto", "exacto", "ese", "esa", "ese mismo",
    "así es", "es correcto", "sí es", "si es", "claro", "perfecto"
]

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
def build_system_prompt(products, services, tarifas):
    productos_txt = "\n".join(
        [f"- {p.name} (precio: {p.price}€, url: {p.url})" for p in products]
    )
    servicios_txt = "\n".join(
        [f"- {s.title}: {s.subtitle}" for s in services]
    )
    tarifas_txt = "\n".join(
        [f"- {t.service.title} / {t.title} ({t.price}€)" for t in tarifas]
    )

    return f"""
Eres el asistente virtual de Natursur, una consulta de bienestar, masaje, par biomagnético y asesoramiento nutricional.

Hablas SIEMPRE en español, de forma clara y amable, pensando que muchas personas son mayores y no se saben los nombres exactos de los productos.

TU TAREA:
1. Ayudar a encontrar productos de Herbalife/Natursur.
2. Explicar las diferencias entre productos y servicios.
3. Ayudar a reservar citas cuando el usuario lo pida (si da suficiente información).
4. Ayudar a navegar por la web (enlaces a: /citas/, /perfil/, /productos/, /servicios/).

PRODUCTOS DISPONIBLES:
{productos_txt}

SERVICIOS DISPONIBLES:
{servicios_txt}

TARIFAS DISPONIBLES:
{tarifas_txt}

MUY IMPORTANTE:
SIEMPRE debes responder con UN ÚNICO JSON VÁLIDO, SIN TEXTO EXTRA NI COMENTARIOS.
El formato del JSON debe ser EXACTAMENTE:

{{
  "message": "Texto que verá el usuario, en español, con emojis suaves si quieres.",
  "action": "none" | "open_url" | "create_appointment",
  "target_url": null o una de estas: "/citas/", "/perfil/", "/productos/", "/servicios/",
  "appointment": {{
      "service_name": "nombre del servicio o null",
      "tarifa_title": "título de la tarifa o null",
      "date": "YYYY-MM-DD o null",
      "time": "HH:MM o null"
  }}
}}

REGLAS:
- Si solo estás contestando una duda y no hace falta hacer nada más, usa action = "none".
- Si el usuario pregunta cómo ver sus citas, o cómo entrar al perfil, etc., usa action = "open_url" y target_url adecuado, por ejemplo "/citas/" o "/perfil/".
- Si el usuario pide directamente una cita y te da servicio, fecha y hora, usa action = "create_appointment" y rellena appointment.
- Si falta información para crear la cita (por ejemplo falta el horario), en "message" pídele esos datos extra y usa action = "none".
- Para escoger productos, usa la lista de productos anterior e intenta adivinar aunque el usuario diga "batido para adelgazar", "ese acondicionador del pelo", etc.
"""

@csrf_exempt
def api_assistant(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    user_message = body.get("message", "").strip()
    if not user_message:
        return JsonResponse({"error": "Mensaje vacío"}, status=400)

    # Recuperar historial
    conversation = request.session.get("assistant_chat", [])

    # Cargar catálogo
    products = Product.objects.all()
    services = Service.objects.all()
    tarifas = Tarifa.objects.all()

    system_prompt = build_system_prompt(products, services, tarifas)

    # Añadir mensaje del usuario
    conversation.append({"role": "user", "content": user_message})

    # Construir historial completo
    messages = [{"role": "system", "content": system_prompt}] + conversation

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.GROQ_MODEL,
        "messages": messages,
        "temperature": 0.4,
    }

    # Llamada a Groq
    try:
        resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
    except Exception as e:
        print("ERROR GROQ:", e)
        print("RESPUESTA GROQ:", resp.text if 'resp' in locals() else 'NO RESP')
        return JsonResponse({
            "reply": "Ahora mismo no puedo responder, inténtalo de nuevo en unos minutos 🙏",
            "redirect_url": None,
        })

    # Guardar respuesta en historial
    conversation.append({"role": "assistant", "content": content})
    request.session["assistant_chat"] = conversation

    # Parsear JSON
    try:
        ai = json.loads(content)
    except Exception:
        return JsonResponse({
            "reply": content,
            "redirect_url": None,
        })

    message = ai.get("message", "No he entendido bien tu mensaje, ¿puedes repetirlo?")
    action = ai.get("action", "none")
    target_url = ai.get("target_url")
    appointment = ai.get("appointment") or {}

    # --- ACCIONES ---

    if action == "create_appointment":
        if not request.user.is_authenticated:
            return JsonResponse({
                "reply": "Para reservar una cita necesitas iniciar sesión 😊",
                "redirect_url": "/login/",
            })

        service_name = appointment.get("service_name")
        tarifa_title = appointment.get("tarifa_title")
        date = appointment.get("date")
        time = appointment.get("time")

        if not (service_name and tarifa_title and date and time):
            return JsonResponse({
                "reply": "Me falta algún dato para completar tu cita (servicio, tarifa, fecha u hora). ¿Puedes confirmarlo?",
                "redirect_url": None,
            })

        service = Service.objects.filter(title__icontains=service_name).first()
        if not service:
            return JsonResponse({
                "reply": f"No encuentro el servicio '{service_name}'. ¿Puedes revisarlo?",
                "redirect_url": None,
            })

        tarifa = Tarifa.objects.filter(service=service, title__icontains=tarifa_title).first()
        if not tarifa:
            return JsonResponse({
                "reply": f"No encuentro la tarifa '{tarifa_title}' para {service.title}. ¿Cuál eliges?",
                "redirect_url": None,
            })

        Cita.objects.create(
            user=request.user.profile,
            service=service,
            tarifa=tarifa,
            date=date,
            time=time,
        )

        return JsonResponse({
            "reply": f"Cita reservada para *{service.title}* — {tarifa.title} el {date} a las {time} 🗓️✨",
            "redirect_url": "/citas/",
        })

    if action == "open_url" and target_url:
        return JsonResponse({
            "reply": message,
            "redirect_url": target_url,
        })

    return JsonResponse({
        "reply": message,
        "redirect_url": None,
    })
