from django.db import transaction
from django.db.models import Sum
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
        cuenta_vieja = transaccion.cuenta
        monto_viejo = transaccion.monto
        tipo_viejo = transaccion.tipo

        cuenta_nueva = nuevos_datos.get('cuenta', cuenta_vieja)
        monto_nuevo = nuevos_datos.get('monto', monto_viejo)
        tipo_nuevo = nuevos_datos.get('tipo', tipo_viejo)

        with transaction.atomic():
            if cuenta_vieja:
                if tipo_viejo == 'ingreso':
                    cuenta_vieja.saldo -= monto_viejo
                elif tipo_viejo == 'gasto':
                    cuenta_vieja.saldo += monto_viejo
                cuenta_vieja.save()

            if cuenta_nueva and cuenta_vieja and cuenta_nueva.id == cuenta_vieja.id:
                cuenta_nueva.refresh_from_db()

            if cuenta_nueva and tipo_nuevo == 'gasto' and cuenta_nueva.saldo < monto_nuevo:
                raise serializers.ValidationError({
                    "monto": f"Saldo insuficiente en la cuenta '{cuenta_nueva.nombre}'. Saldo disponible: ${cuenta_nueva.saldo}"
                })

            if cuenta_nueva:
                if tipo_nuevo == 'ingreso':
                    cuenta_nueva.saldo += monto_nuevo
                elif tipo_nuevo == 'gasto':
                    cuenta_nueva.saldo -= monto_nuevo
                cuenta_nueva.save()

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

    @staticmethod
    def obtener_reporte_financiero(usuario_id, cuenta_id=None):
        from app.models import CuentaBancaria
        from .models import Transaccion

        cuentas = CuentaBancaria.objects.filter(usuario_id=usuario_id)
        if cuenta_id:
            cuentas = cuentas.filter(id=cuenta_id)

        saldo_total = sum(float(c.saldo) for c in cuentas)

        transacciones = Transaccion.objects.filter(usuario_id=usuario_id)
        if cuenta_id:
            transacciones = transacciones.filter(cuenta_id=cuenta_id)

        total_ingresos = transacciones.filter(tipo__iexact='ingreso').aggregate(Sum('monto'))['monto__sum'] or 0
        total_gastos = transacciones.filter(tipo__iexact='gasto').aggregate(Sum('monto'))['monto__sum'] or 0

        gastos_qs = transacciones.filter(tipo__iexact='gasto')
        
        desglose_categorias = {}
        gastos_hormiga_estimados = 0

        for t in gastos_qs:
            monto = float(t.monto)
            cat = t.descripcion.split(' - ')[0] if ' - ' in t.descripcion else t.descripcion
            desglose_categorias[cat] = desglose_categorias.get(cat, 0) + monto

            if monto <= 20000 and cat in ['Alimentación', 'Entretenimiento', 'Otra']:
                gastos_hormiga_estimados += monto

        return {
            "resumen_general": {
                "balance_total": round(saldo_total, 2),
                "total_ingresos": round(float(total_ingresos), 2),
                "total_gastos": round(float(total_gastos), 2),
                "gastos_hormiga_estimados": round(gastos_hormiga_estimados, 2),
            },
            "desglose_categorias": [
                {"categoria": k, "monto": round(v, 2)}
                for k, v in sorted(desglose_categorias.items(), key=lambda x: x[1], reverse=True)
            ]
        }
