from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from accounts.forms import AdminRegisterForm, UserRegisterForm


def _style_form(form):
    """Aplica clases y placeholders comunes a formularios de auth."""
    for name, field in form.fields.items():
        field.widget.attrs.update(
            {"class": "input-control", "placeholder": field.label}
        )


def home(request):
    return render(request, "core/index.html")


def login_view(request):
    """Login de usuarios y administradores usando el sistema de auth de Django."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}")
            return redirect("home")
        messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = AuthenticationForm()
    _style_form(form)
    return render(request, "core/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente")
    return redirect("home")


def register_user(request):
    """Registro para clientes/usuarios estándar."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada. Ya puedes iniciar sesión.")
            return redirect("login")
        messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = UserRegisterForm()
    _style_form(form)
    return render(request, "core/register_user.html", {"form": form})


def register_admin(request):
    """Registro para crear cuentas con permisos de staff (administración interna)."""
    if request.method == "POST":
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Administrador creado. Ya puedes iniciar sesión.")
            return redirect("login")
        messages.error(request, "Revisa los datos ingresados.")
    else:
        form = AdminRegisterForm()
    _style_form(form)
    return render(request, "core/register_admin.html", {"form": form})
