from django.urls import path
from .views import InfoCuentasView, RegistrarCuentaView

urlpatterns = [
    path('', InfoCuentasView.as_view(), name='listar_cuentas'),
    path('registrar/', RegistrarCuentaView.as_view(), name='registrar_cuenta'),
]
