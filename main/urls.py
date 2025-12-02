from django.urls import path
from . import views

urlpatterns = [
    # HOME
    path("", views.home, name="home"),

    # SERVICIOS
    path("servicios/", views.servicios_list, name="servicios_list"),
    path("servicios/<int:service_id>/", views.servicio_detalle, name="servicio_detalle"),

    # PRODUCTOS
    path("productos/", views.productos_list, name="productos_list"),

    # CITAS
    path("citas/", views.citas_list, name="citas_list"),
    path("citas/crear/<int:service_id>/<int:tarifa_id>/", views.crear_cita, name="crear_cita"),
    path("citas/<int:cita_id>/editar/", views.editar_cita, name="editar_cita"),
    path("citas/<int:cita_id>/cancelar/", views.cancelar_cita, name="cancelar_cita"),

    # LOGIN / REGISTER
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # PERFIL
    path("perfil/", views.perfil_view, name="perfil"),
    path("perfil/editar/", views.perfil_editar, name="perfil_editar"),

    # SOBRE NOSOTROS
    path("sobre-nosotros/", views.sobre_nosotros, name="sobre_nosotros"),
]
