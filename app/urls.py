from django.urls import path
from .views import ListaCuentasView, RegistroCuentaView, DetalleCuentaBancariaView

urlpatterns = [
    path('cuentas/', ListaCuentasView.as_view(), name='lista_cuentas'),
    path('cuentas/registrar/', RegistroCuentaView.as_view(), name='registro_cuenta'),
    path('cuentas/<int:pk>/', DetalleCuentaBancariaView.as_view(), name='detalle_cuenta'),
]
