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

class Suscripcion(models.Model):
    FRECUENCIA_CHOICES = [
        ('Mensual', 'Mensual'),
        ('Anual', 'Anual'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='suscripciones')
    cuenta = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE, related_name='suscripciones')
    nombre = models.CharField(max_length=100) # ej: "Netflix", "Software X"
    servicio_preset = models.CharField(max_length=50, default='otro') # ej: 'netflix', 'spotify', 'otro'
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIA_CHOICES, default='Mensual')
    fecha_proximo_pago = models.DateField()

    def __str__(self):
        return f"{self.nombre} (${self.monto}) - {self.cuenta.nombre}"
