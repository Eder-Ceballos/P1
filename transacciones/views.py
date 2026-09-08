from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TransaccionSerializer
from .services import TransaccionService

class RegistroTransaccionView(APIView):
    """Endpoint para que React registre un gasto o ingreso manual."""
    
    def post(self, request):
        serializer = TransaccionSerializer(data=request.data)
        
        if serializer.is_valid():
            # Delegamos la creación al servicio
            transaccion = TransaccionService.crear_transaccion(serializer.validated_data)
            
            # Devolvemos el objeto creado en formato JSON
            response_serializer = TransaccionSerializer(transaccion)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
