from django.db import models

class CuentaBancaria(models.Model):
    TIPOS_CUENTA = [
        ('Ahorros', 'Ahorros'),
        ('Corriente', 'Corriente'),
        ('Credito', 'Credito'),
    ]

    # Usamos string para evitar importación circular
    usuario = models.ForeignKey('transacciones.Usuario', on_delete=models.CASCADE, related_name='cuentas')
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPOS_CUENTA)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - ${self.saldo}"
