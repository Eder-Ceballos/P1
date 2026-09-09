from django.db import models

# Create your models here.

from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=150)
    # Aquí irá la autenticación real luego

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class CuentaBancaria(models.Model):
    """Módulo futuro: Tus compañeros expandirán esto con saldo, banco, etc."""
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Transaccion(models.Model):
    TIPO_CHOICES = [('ingreso', 'Ingreso'), ('gasto', 'Gasto')]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255, blank=True)
    
    # Claves foráneas flexibles (pueden ser nulas por ahora)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    cuenta = models.ForeignKey(CuentaBancaria, on_delete=models.SET_NULL, null=True, blank=True)
