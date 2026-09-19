from django.db import transaction
from rest_framework import serializers
from .models import Transaccion

class TransaccionService:
    @staticmethod
    def crear_transaccion(datos_validados):
        cuenta = datos_validados.get('cuenta')
        monto = datos_validados.get('monto')
        tipo = datos_validados.get('tipo')

        if cuenta:
            if tipo == 'gasto' and cuenta.saldo < monto:
                raise serializers.ValidationError({
                    "monto": f"Saldo insuficiente en la cuenta '{cuenta.nombre}'. Saldo actual: ${cuenta.saldo}"
                })

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

    @staticmethod
    def actualizar_transaccion(transaccion, nuevos_datos):
        """
        Permite la edición completa de una transacción, recalculando el saldo 
        de la cuenta original y la nueva cuenta si hubo un cambio de cuenta de origen.
        """
        cuenta_vieja = transaccion.cuenta
        monto_viejo = transaccion.monto
        tipo_viejo = transaccion.tipo

        cuenta_nueva = nuevos_datos.get('cuenta', cuenta_vieja)
        monto_nuevo = nuevos_datos.get('monto', monto_viejo)
        tipo_nuevo = nuevos_datos.get('tipo', tipo_viejo)

        with transaction.atomic():
            # 1. Revertir el impacto de la transacción original en la cuenta vieja
            if cuenta_vieja:
                if tipo_viejo == 'ingreso':
                    cuenta_vieja.saldo -= monto_viejo
                elif tipo_viejo == 'gasto':
                    cuenta_vieja.saldo += monto_viejo
                cuenta_vieja.save()

            # Refrescar instancia si la cuenta de origen y destino es la misma
            if cuenta_nueva and cuenta_vieja and cuenta_nueva.id == cuenta_vieja.id:
                cuenta_nueva.refresh_from_db()

            # 2. Validar si la cuenta nueva tiene saldo suficiente ante el nuevo gasto
            if cuenta_nueva and tipo_nuevo == 'gasto' and cuenta_nueva.saldo < monto_nuevo:
                raise serializers.ValidationError({
                    "monto": f"Saldo insuficiente en la cuenta '{cuenta_nueva.nombre}'. Saldo disponible: ${cuenta_nueva.saldo}"
                })

            # 3. Aplicar el impacto de la nueva transacción en la cuenta nueva
            if cuenta_nueva:
                if tipo_nuevo == 'ingreso':
                    cuenta_nueva.saldo += monto_nuevo
                elif tipo_nuevo == 'gasto':
                    cuenta_nueva.saldo -= monto_nuevo
                cuenta_nueva.save()

            # 4. Actualizar todos los campos modificados en la transacción
            for campo, valor in nuevos_datos.items():
                setattr(transaccion, campo, valor)
            transaccion.save()

        return transaccion

    @staticmethod
    def eliminar_transaccion(transaccion):
        cuenta = transaccion.cuenta
        monto = transaccion.monto
        tipo = transaccion.tipo

        with transaction.atomic():
            if cuenta:
                if tipo == 'ingreso':
                    cuenta.saldo -= monto
                elif tipo == 'gasto':
                    cuenta.saldo += monto
                cuenta.save()

            transaccion.delete()
