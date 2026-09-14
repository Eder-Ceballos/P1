from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    # Referencia mediante cadena 'app.CuentaBancaria'
    cuenta = models.ForeignKey('app.CuentaBancaria', on_delete=models.CASCADE, related_name='transacciones', null=True, blank=True)

    def __str__(self):
        return f"{self.tipo.upper()}: ${self.monto} en {self.cuenta.nombre}"
