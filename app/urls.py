from django.urls import path
from .views import ListaCuentasView, RegistroCuentaView, DetalleCuentaView

urlpatterns = [
    path('cuentas/', ListaCuentasView.as_view(), name='lista_cuentas'),
    path('cuentas/registrar/', RegistroCuentaView.as_view(), name='registrar_cuenta'),
    path('cuentas/<int:pk>/', DetalleCuentaView.as_view(), name='detalle_cuenta'),
]
