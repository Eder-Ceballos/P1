from django.urls import path
from .views import (
    HistorialTransaccionesView, 
    RegistroTransaccionView, 
    DetalleTransaccionView, 
    RegistrarUsuarioView,
    LoginUsuarioView
)

urlpatterns = [
    path('transacciones/', HistorialTransaccionesView.as_view(), name='historial_transacciones'),
    path('transacciones/registrar/', RegistroTransaccionView.as_view(), name='registrar_transaccion'),
    path('transacciones/<int:pk>/', DetalleTransaccionView.as_view(), name='detalle_transaccion'),
    path('transacciones/registrar-usuario/', RegistrarUsuarioView.as_view(), name='registrar_usuario'),
    path('transacciones/login-usuario/', LoginUsuarioView.as_view(), name='login_usuario'),
]
