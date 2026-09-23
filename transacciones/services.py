from django.db.models import Sum, Count
from .models import Transaccion

class TransaccionService:
    @staticmethod
    def obtener_reporte_financiero(usuario_id, cuenta_id=None):
        query = Transaccion.objects.filter(usuario_id=usuario_id)

        if cuenta_id:
            query = query.filter(cuenta_id=cuenta_id)

        # 1. Totales de Ingresos, Gastos y Transferencias
        ingresos_total = query.filter(tipo='ingreso').aggregate(total=Sum('monto'))['total'] or 0
        gastos_total = query.filter(tipo='gasto').aggregate(total=Sum('monto'))['total'] or 0
        
        # Para transferencias, calculamos enviadas vs recibidas
        transferencias_query = query.filter(tipo='transferencia')
        trans_enviadas = transferencias_query.filter(descripcion__icontains='enviada').aggregate(total=Sum('monto'))['total'] or 0
        trans_recibidas = transferencias_query.filter(descripcion__icontains='recibida').aggregate(total=Sum('monto'))['total'] or 0

        total_transacciones = query.count()

        # 2. Desglose reciente de transacciones para analíticas
        recientes = query.order_by('-fecha')[:10]
        desglose_reciente = [
            {
                'id': t.id,
                'monto': float(t.monto),
                'tipo': t.tipo,
                'descripcion': t.descripcion or 'Sin descripción',
                'cuenta': t.cuenta.nombre,
                'fecha': t.fecha.strftime('%Y-%m-%d %H:%M')
            }
            for t in recientes
        ]

        return {
            'resumen': {
                'total_ingresos': float(ingresos_total),
                'total_gastos': float(gastos_total),
                'balance_neto': float(ingresos_total) - float(gastos_total),
                'total_transferencias_enviadas': float(trans_enviadas),
                'total_transferencias_recibidas': float(trans_recibidas),
                'cantidad_transacciones': total_transacciones
            },
            'desglose_reciente': desglose_reciente
        }
