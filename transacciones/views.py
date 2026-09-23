from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from app.models import CuentaBancaria
from .models import Transaccion
from .serializers import TransaccionSerializer
from .services import TransaccionService
from django.contrib.auth.models import User

class ListaTransaccionesView(APIView):
    """Endpoint para listar y registrar transacciones individuales."""

    def get(self, request):
        usuario_id = request.query_params.get('usuario')
        cuenta_id = request.query_params.get('cuenta')
        tipo = request.query_params.get('tipo')

        transacciones = Transaccion.objects.all()

        if usuario_id:
            transacciones = transacciones.filter(usuario_id=usuario_id)
        if cuenta_id:
            transacciones = transacciones.filter(cuenta_id=cuenta_id)
        if tipo:
            transacciones = transacciones.filter(tipo=tipo)

        transacciones = transacciones.order_by('-fecha')
        serializer = TransaccionSerializer(transacciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransaccionSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                transaccion = serializer.save()
                cuenta = transaccion.cuenta
                
                # Actualizar saldo de acuerdo al movimiento
                if transaccion.tipo == 'ingreso':
                    cuenta.saldo = float(cuenta.saldo) + float(transaccion.monto)
                elif transaccion.tipo == 'gasto':
                    cuenta.saldo = float(cuenta.saldo) - float(transaccion.monto)
                
                cuenta.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetalleTransaccionView(APIView):
    """Endpoint para obtener o eliminar una transacción específica."""

    def get(self, request, pk):
        transaccion = get_object_or_404(Transaccion, pk=pk)
        serializer = TransaccionSerializer(transaccion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        transaccion = get_object_or_404(Transaccion, pk=pk)
        
        with transaction.atomic():
            cuenta = transaccion.cuenta
            if transaccion.tipo in ['ingreso', 'transferencia_recibida']:
                cuenta.saldo = float(cuenta.saldo) - float(transaccion.monto)
            elif transaccion.tipo in ['gasto', 'transferencia']:
                cuenta.saldo = float(cuenta.saldo) + float(transaccion.monto)
            
            cuenta.save()
            transaccion.delete()

        return Response({'mensaje': 'Transacción eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)


class ReporteFinancieroView(APIView):
    def get(self, request):
        usuario_id = request.query_params.get('usuario')
        cuenta_id = request.query_params.get('cuenta')

        if not usuario_id:
            return Response({'error': 'El parámetro usuario es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        reporte = TransaccionService.obtener_reporte_financiero(
            usuario_id=int(usuario_id),
            cuenta_id=int(cuenta_id) if cuenta_id else None
        )
        return Response(reporte, status=status.HTTP_200_OK)


class TransferenciaEntreCuentasView(APIView):
    """Endpoint atómico para realizar transferencias de saldo entre dos cuentas."""

    def post(self, request):
        usuario_id = request.data.get('usuario')
        cuenta_origen_id = request.data.get('cuenta_origen')
        cuenta_destino_id = request.data.get('cuenta_destino')
        monto_str = request.data.get('monto')
        descripcion = request.data.get('descripcion', '').strip()

        if not all([usuario_id, cuenta_origen_id, cuenta_destino_id, monto_str]):
            return Response(
                {'error': 'Todos los campos son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if str(cuenta_origen_id) == str(cuenta_destino_id):
            return Response(
                {'error': 'La cuenta de origen y destino deben ser distintas.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            monto = float(monto_str)
            if monto <= 0:
                return Response({'error': 'El monto debe ser un valor positivo.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'El monto ingresado no es válido.'}, status=status.HTTP_400_BAD_REQUEST)

        cuenta_origen = get_object_or_404(CuentaBancaria, pk=cuenta_origen_id, usuario_id=usuario_id)
        cuenta_destino = get_object_or_404(CuentaBancaria, pk=cuenta_destino_id, usuario_id=usuario_id)

        if float(cuenta_origen.saldo) < monto:
            return Response(
                {'error': f'Saldo insuficiente en {cuenta_origen.nombre}. Disponible: ${cuenta_origen.saldo:,.0f}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Descontar y acreditar saldos
            cuenta_origen.saldo = float(cuenta_origen.saldo) - monto
            cuenta_destino.saldo = float(cuenta_destino.saldo) + monto

            cuenta_origen.save()
            cuenta_destino.save()

            nota_origen = f"Transferencia enviada a {cuenta_destino.nombre}"
            nota_destino = f"Transferencia recibida de {cuenta_origen.nombre}"
            if descripcion:
                nota_origen += f" ({descripcion})"
                nota_destino += f" ({descripcion})"

            # Registro de trazabilidad con tipo 'transferencia'
            Transaccion.objects.create(
                usuario_id=usuario_id,
                cuenta=cuenta_origen,
                monto=monto,
                tipo='transferencia',
                descripcion=nota_origen
            )

            Transaccion.objects.create(
                usuario_id=usuario_id,
                cuenta=cuenta_destino,
                monto=monto,
                tipo='transferencia',
                descripcion=nota_destino
            )

        return Response(
            {
                'mensaje': 'Transferencia realizada con éxito.',
                'saldo_origen': cuenta_origen.saldo,
                'saldo_destino': cuenta_destino.saldo
            },
            status=status.HTTP_200_OK
        )

class LoginUsuarioView(APIView):
    """Obtiene o crea automáticamente el usuario en la tabla auth_user de Django."""

    def post(self, request):
        nombre = request.data.get('nombre', '').strip()
        if not nombre:
            return Response({'error': 'El nombre de usuario es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Crear o recuperar usuario en auth_user
        username_clean = nombre.lower().replace(' ', '_')
        usuario, _ = User.objects.get_or_create(
            username=username_clean,
            defaults={'first_name': nombre}
        )

        return Response({
            'id': usuario.id,
            'nombre': usuario.first_name or usuario.username,
            'username': usuario.username
        }, status=status.HTTP_200_OK)
