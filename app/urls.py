from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("cuentas", views.info_cuentas, name="cuentas"),
    path("registrar", views.registrar, name="registrar"),
]
