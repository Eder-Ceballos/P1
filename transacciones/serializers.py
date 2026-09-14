from rest_framework import serializers
from django.db import transaction
from .models import Transaccion

class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = ['id', 'usuario', 'cuenta', 'categoria', 'monto', 'tipo', 'descripcion', 'fecha']
        read_only_fields = ['fecha']

    def create(self, validated_data):
        cuenta = validated_data['cuenta']
        monto = validated_data['monto']
        tipo = validated_data['tipo']

        # Validar si tiene saldo suficiente en caso de gasto
        if tipo == 'gasto' and cuenta.saldo < monto:
            raise serializers.ValidationError({
                "monto": f"Saldo insuficiente en la cuenta '{cuenta.nombre}'. Saldo actual: ${cuenta.saldo}"
            })

        # Transacción atómica en la base de datos
        with transaction.atomic():
            if tipo == 'ingreso':
                cuenta.saldo += monto
            elif tipo == 'gasto':
                cuenta.saldo -= monto
            
            cuenta.save()
            transaccion_instancia = Transaccion.objects.create(**validated_data)

        return transaccion_instancia
