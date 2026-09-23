from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CuentaBancaria
from .serializers import CuentaBancariaSerializer

class ListaCuentasView(APIView):
    """Listar todas las cuentas bancarias registradas."""
    def get(self, request):
        cuentas = CuentaBancaria.objects.all()
        serializer = CuentaBancariaSerializer(cuentas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegistroCuentaView(APIView):
    """Registrar una nueva cuenta bancaria."""
    def post(self, request):
        serializer = CuentaBancariaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetalleCuentaBancariaView(APIView):
    """Endpoint para obtener, actualizar o eliminar una cuenta bancaria especifica."""

    def delete(self, request, pk):
        cuenta = get_object_or_404(CuentaBancaria, pk=pk)
        
        with transaction.atomic():
            # Eliminamos las transacciones asociadas a esta cuenta para no dejar huerfanos los registros
            Transaccion.objects.filter(cuenta=cuenta).delete()
            cuenta.delete()

        return Response(
            {"mensaje": "Cuenta bancaria y sus transacciones asociadas eliminadas correctamente."},
            status=status.HTTP_204_NO_CONTENT
        )
