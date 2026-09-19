from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Transaccion
from .serializers import TransaccionSerializer
from .services import TransaccionService

class RegistroTransaccionView(APIView):
    """Endpoint para registrar un gasto o ingreso manual."""
    def post(self, request):
        serializer = TransaccionSerializer(data=request.data)
        if serializer.is_valid():
            transaccion = TransaccionService.crear_transaccion(serializer.validated_data)
            response_serializer = TransaccionSerializer(transaccion)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistorialTransaccionesView(APIView):
    """Endpoint para listar todo el historial de transacciones."""
    def get(self, request):
        transacciones = Transaccion.objects.all().order_by('-fecha', '-id')
        serializer = TransaccionSerializer(transacciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DetalleTransaccionView(APIView):
    """Endpoint para ver, actualizar o eliminar una transacción individual."""
    def get(self, request, pk):
        transaccion = get_object_or_404(Transaccion, pk=pk)
        serializer = TransaccionSerializer(transaccion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        transaccion = get_object_or_404(Transaccion, pk=pk)
        serializer = TransaccionSerializer(transaccion, data=request.data, partial=True)
        if serializer.is_valid():
            transaccion_actualizada = TransaccionService.actualizar_transaccion(transaccion, serializer.validated_data)
            response_serializer = TransaccionSerializer(transaccion_actualizada)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transaccion = get_object_or_404(Transaccion, pk=pk)
        TransaccionService.eliminar_transaccion(transaccion)
        return Response(
            {"mensaje": "Transacción eliminada y saldo de la cuenta reajustado correctamente."},
            status=status.HTTP_204_NO_CONTENT
        )
