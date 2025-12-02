from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as DjangoUser

from main.models import Service, Product, Tarifa, Cita, User as Profile


# ------------------------------------
# HOME
# ------------------------------------
def home(request):
    services = Service.objects.all()
    products = Product.objects.all()[:8]
    return render(request, "home.html", {
        "services": services,
        "products": products,
    })


# ------------------------------------
# SERVICIOS
# ------------------------------------
def servicios_list(request):
    servicios = Service.objects.all()
    tarifas = Tarifa.objects.all()

    return render(request, "servicios/list.html", {
        "servicios": servicios,
        "tarifas": tarifas,
    })


def servicio_detalle(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    tarifas = Tarifa.objects.filter(service=service)
    return render(request, "servicios/detalle.html", {
        "service": service,
        "tarifas": tarifas,
    })


# ------------------------------------
# PRODUCTOS
# ------------------------------------
def productos_list(request):
    productos = Product.objects.all()

    # Handle search query
    query = request.GET.get('q')
    if query:
        productos = productos.filter(name__icontains=query)

    # Handle sorting
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        productos = productos.order_by('price')
    elif sort == 'price_desc':
        productos = productos.order_by('-price')

    return render(request, "productos/list.html", {"productos": productos, "request": request})


# ------------------------------------
# CITAS
# ------------------------------------
@login_required
def citas_list(request):
    citas = Cita.objects.filter(user=request.user.profile)
    return render(request, "citas/list.html", {"citas": citas})


@login_required
def crear_cita(request, service_id, tarifa_id):
    service = get_object_or_404(Service, id=service_id)
    tarifa = get_object_or_404(Tarifa, id=tarifa_id)

    services = Service.objects.all()
    tarifas = Tarifa.objects.filter(service=service)

    if request.method == "POST":
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        servicio_id = request.POST.get("service_id")
        tarifa_id = request.POST.get("tarifa_id")

        service = Service.objects.get(id=servicio_id)
        tarifa = Tarifa.objects.get(id=tarifa_id)

        Cita.objects.create(
            user=request.user.profile,
            service=service,
            tarifa=tarifa,
            date=fecha,
            time=hora,
        )
        return redirect("citas_list")

    return render(request, "citas/crear.html", {
        "service": service,
        "tarifa": tarifa,
        "services": services,
        "tarifas": tarifas,
    })

@login_required
def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, user=request.user.profile)

    if request.method == "POST":
        cita.date = request.POST.get("fecha")
        cita.time = request.POST.get("hora")
        cita.save()
        return redirect("citas_list")

    return render(request, "citas/editar.html", {"cita": cita})


@login_required
def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, user=request.user.profile)

    if request.method == "POST":
        cita.estado = "cancelada"
        cita.save()
        return redirect("citas_list")

    return render(request, "citas/cancelar.html", {"cita": cita})


# ------------------------------------
# LOGIN
# ------------------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")

    return render(request, "login.html")


# ------------------------------------
# REGISTER
# ------------------------------------
def register_view(request):
    if request.method == "POST":
        data = request.POST

        # Crear usuario Django
        django_user = DjangoUser.objects.create_user(
            username=data["username"],
            password=data["password"],
            email=data["mail"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )

        # Crear perfil asociado
        Profile.objects.create(
            django_user=django_user,
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            mail=data["mail"],
            direccion=data["direccion"],
            postal_code=data["postal_code"],
            age=data["age"],
            telephone_number=data["telephone_number"],
            password=data["password"],
        )

        login(request, django_user)
        return redirect("home")

    return render(request, "register.html")

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect("/")


# ------------------------------------
# PERFIL
# ------------------------------------
@login_required
def perfil_view(request):
    profile = request.user.profile
    return render(request, "perfil.html", {"user": profile})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def perfil_editar(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.first_name = request.POST.get("first_name")
        profile.last_name = request.POST.get("last_name")
        profile.direccion = request.POST.get("direccion")
        profile.postal_code = request.POST.get("postal_code")
        profile.age = request.POST.get("age")
        profile.telephone_number = request.POST.get("telephone_number")

        # guardar imagen si existe
        if "image" in request.FILES:
            profile.image = request.FILES["image"]

        profile.save()
        return redirect("/perfil/")

    return render(request, "perfil_editar.html", {"user": profile})


# ------------------------------------
# SOBRE NOSOTROS
# ------------------------------------
def sobre_nosotros(request):
    return render(request, "sobre_nosotros.html")
