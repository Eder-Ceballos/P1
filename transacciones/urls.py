from django.urls import path
from .views import RegistroTransaccionView, HistorialTransaccionesView, DetalleTransaccionView

urlpatterns = [
    path('', HistorialTransaccionesView.as_view(), name='historial_transacciones'),
    path('registrar/', RegistroTransaccionView.as_view(), name='registrar_transaccion'),
    path('<int:pk>/', DetalleTransaccionView.as_view(), name='detalle_transaccion'),
]
