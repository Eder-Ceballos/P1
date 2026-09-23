from django.db import models
from transacciones.models import Usuario

class CuentaBancaria(models.Model):
    TIPO_CHOICES = [
        ('Ahorros', 'Cuenta de Ahorros'),
        ('Corriente', 'Cuenta Corriente'),
        ('Billetera Digital', 'Billetera Digital'),
        ('Tarjeta de Crédito', 'Tarjeta de Crédito'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='cuentas')
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, default='Ahorros')
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Nuevo campo para presupuestos y límites por cuenta
    tope_gasto_mensual = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nombre} - {self.usuario.nombre}"
