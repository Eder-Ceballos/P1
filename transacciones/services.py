from .models import Transaccion, Usuario, Categoria, CuentaBancaria

class TransaccionService:
    @staticmethod
    def crear_transaccion(data):
        """
        Recibe un diccionario con los datos validados y ejecuta la lógica de negocio.
        Aquí se conectará a futuro la lógica de actualización de saldos de cuentas.
        """
        transaccion = Transaccion.objects.create(**data)
        
        # FUTURO: Si la transacción es un gasto y tiene cuenta asociada,
        # llamar a un servicio de cuentas para actualizar el saldo.
        # if transaccion.cuenta and transaccion.tipo == 'gasto':
        #     CuentaService.descontar_saldo(transaccion.cuenta.id, transaccion.monto)
            
        return transaccion
