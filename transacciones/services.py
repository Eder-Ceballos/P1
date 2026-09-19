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
        """Ajusta el saldo de la cuenta recalculando la diferencia al editar una transacción."""
        cuenta_antigua = transaccion.cuenta
        monto_antiguo = transaccion.monto
        tipo_antiguo = transaccion.tipo

        cuenta_nueva = nuevos_datos.get('cuenta', cuenta_antigua)
        monto_nuevo = nuevos_datos.get('monto', monto_antiguo)
        tipo_nuevo = nuevos_datos.get('tipo', tipo_antiguo)

        with transaction.atomic():
            # 1. Revertir el efecto de la transacción vieja en la cuenta antigua
            if tipo_antiguo == 'ingreso':
                cuenta_antigua.saldo -= monto_antiguo
            elif tipo_antiguo == 'gasto':
                cuenta_antigua.saldo += monto_antiguo
            cuenta_antigua.save()

            # Refresh por si la cuenta es la misma
            if cuenta_nueva.id == cuenta_antigua.id:
                cuenta_nueva.refresh_from_db()

            # 2. Validar que la cuenta nueva tenga fondos si la edición resulta en un gasto
            if tipo_nuevo == 'gasto' and cuenta_nueva.saldo < monto_nuevo:
                # Si no alcanza, deshacemos revirtiendo la operación
                raise serializers.ValidationError({
                    "monto": f"Saldo insuficiente para realizar el cambio en la cuenta '{cuenta_nueva.nombre}'."
                })

            # 3. Aplicar el efecto de la nueva transacción
            if tipo_nuevo == 'ingreso':
                cuenta_nueva.saldo += monto_nuevo
            elif tipo_nuevo == 'gasto':
                cuenta_nueva.saldo -= monto_nuevo
            cuenta_nueva.save()

            # 4. Actualizar los campos del modelo
            for campo, valor in nuevos_datos.items():
                setattr(transaccion, campo, valor)
            transaccion.save()

        return transaccion

    @staticmethod
    def eliminar_transaccion(transaccion):
        """Devuelve/reajusta el dinero a la cuenta antes de borrar la transacción."""
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
