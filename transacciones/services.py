from django.db import transaction
from rest_framework import serializers
from .models import Transaccion, Usuario, Categoria
from app.models import CuentaBancaria

class TransaccionService:
    @staticmethod
    def crear_transaccion(datos_validados):
        cuenta = datos_validados.get('cuenta')
        monto = datos_validados.get('monto')
        tipo = datos_validados.get('tipo')

        if cuenta:
            # Validar fondos en caso de gasto
            if tipo == 'gasto' and cuenta.saldo < monto:
                raise serializers.ValidationError({
                    "monto": f"Saldo insuficiente en la cuenta '{cuenta.nombre}'. Saldo actual: ${cuenta.saldo}"
                })

            # Actualización atómica del saldo en la base de datos
            with transaction.atomic():
                if tipo == 'ingreso':
                    cuenta.saldo += monto
                elif tipo == 'gasto':
                    cuenta.saldo -= monto
                
                cuenta.save()
                transaccion = Transaccion.objects.create(**datos_validados)
        else:
            transaccion = Transaccion.objects.create(**datos_validados)

        return transaccion
