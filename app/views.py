from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CuentaBancaria
from .serializers import CuentaBancariaSerializer

class InfoCuentasView(APIView):
    def get(self, request):
        cuentas = CuentaBancaria.objects.all()
        serializer = CuentaBancariaSerializer(cuentas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegistrarCuentaView(APIView):
    def post(self, request):
        serializer = CuentaBancariaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetalleCuentaView(APIView):
    def get(self, request, pk):
        cuenta = get_object_or_404(CuentaBancaria, pk=pk)
        serializer = CuentaBancariaSerializer(cuenta)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        cuenta = get_object_or_404(CuentaBancaria, pk=pk)
        cuenta.delete()
        return Response(
            {"mensaje": f"La cuenta '{cuenta.nombre}' ha sido eliminada exitosamente."},
            status=status.HTTP_204_NO_CONTENT
        )
