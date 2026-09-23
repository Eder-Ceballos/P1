from django.urls import path
from .views import (
    ListaCuentasView,
    RegistroCuentaView,
    DetalleCuentaBancariaView,
    ListaSuscripcionesView,
    DetalleSuscripcionView,
    ProcesarAutoDebitosView
)

urlpatterns = [
    path('cuentas/', ListaCuentasView.as_view(), name='lista_cuentas'),
    path('cuentas/registrar/', RegistroCuentaView.as_view(), name='registro_cuenta'),
    path('cuentas/<int:pk>/', DetalleCuentaBancariaView.as_view(), name='detalle_cuenta'),
    
    path('suscripciones/', ListaSuscripcionesView.as_view(), name='lista_suscripciones'),
    path('suscripciones/<int:pk>/', DetalleSuscripcionView.as_view(), name='detalle_suscripcion'),
    path('suscripciones/procesar-autodebitos/', ProcesarAutoDebitosView.as_view(), name='procesar_autodebitos'),
]
