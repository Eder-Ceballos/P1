from django.urls import path
from .views import RegistroTransaccionView

urlpatterns = [
    path('registrar/', RegistroTransaccionView.as_view(), name='registrar_transaccion'),
]
