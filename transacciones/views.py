from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Transaccion
from .models import Usuario
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
    """Endpoint para listar el historial de transacciones con opción de filtrado."""
    def get(self, request):
        transacciones = Transaccion.objects.all().order_by('-fecha', '-id')

        # Obtener parámetros de filtro de la URL
        tipo = request.query_params.get('tipo')       # 'ingreso' o 'gasto'
        cuenta_id = request.query_params.get('cuenta') # ID de la cuenta

        if tipo:
            transacciones = transacciones.filter(tipo__iexact=tipo)
        if cuenta_id:
            transacciones = transacciones.filter(cuenta_id=cuenta_id)

        serializer = TransaccionSerializer(transacciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DetalleTransaccionView(APIView):
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

class RegistrarUsuarioView(APIView):
    """Endpoint para registrar un nuevo usuario."""
    def post(self, request):
        nombre = request.data.get('nombre')
        if not nombre or not nombre.strip():
            return Response({'error': 'El nombre de usuario es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
        
        nombre_clean = nombre.strip()
        if Usuario.objects.filter(nombre__iexact=nombre_clean).exists():
            return Response({'error': 'El usuario ya existe. Intenta iniciar sesión.'}, status=status.HTTP_400_BAD_REQUEST)
            
        usuario = Usuario.objects.create(nombre=nombre_clean)
        return Response({'id': usuario.id, 'nombre': usuario.nombre}, status=status.HTTP_201_CREATED)

class LoginUsuarioView(APIView):
    """Endpoint para iniciar sesión con un usuario existente."""
    def post(self, request):
        nombre = request.data.get('nombre')
        if not nombre or not nombre.strip():
            return Response({'error': 'Ingresa tu nombre de usuario'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            usuario = Usuario.objects.get(nombre__iexact=nombre.strip())
            return Response({'id': usuario.id, 'nombre': usuario.nombre}, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado. Verifica el nombre o regístrate.'}, status=status.HTTP_404_NOT_FOUND)

class ReporteFinancieroView(APIView):
    """Endpoint para obtener las métricas analíticas preparadas para UI e IA."""
    def get(self, request):
        usuario_id = request.query_params.get('usuario')
        cuenta_id = request.query_params.get('cuenta')
        
        if not usuario_id:
            return Response({'error': 'El parámetro usuario es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
        cuenta_id_int = int(cuenta_id) if cuenta_id else None
        reporte = TransaccionService.obtener_reporte_financiero(int(usuario_id), cuenta_id=cuenta_id_int)
        return Response(reporte, status=status.HTTP_200_OK)
