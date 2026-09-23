from rest_framework import serializers
from .models import CuentaBancaria, Suscripcion

class CuentaBancariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaBancaria
        fields = ['id', 'usuario', 'nombre', 'tipo', 'saldo', 'tope_gasto_mensual']

class SuscripcionSerializer(serializers.ModelSerializer):
    nombre_cuenta = serializers.ReadOnlyField(source='cuenta.nombre')
    tipo_cuenta = serializers.ReadOnlyField(source='cuenta.tipo')

    class Meta:
        model = Suscripcion
        fields = [
            'id', 
            'usuario', 
            'cuenta', 
            'nombre_cuenta', 
            'tipo_cuenta', 
            'nombre', 
            'servicio_preset', 
            'monto', 
            'frecuencia', 
            'fecha_proximo_pago'
        ]
