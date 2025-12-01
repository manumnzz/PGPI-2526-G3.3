from django.urls import path
from . import views

app_name = "social"

urlpatterns = [
    path("links/", views.links, name="links"),
]
