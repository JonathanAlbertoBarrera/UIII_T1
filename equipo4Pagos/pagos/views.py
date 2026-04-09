from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .serializers import ProcesarPagoSerializer, PagoResponseSerializer
from .models import Pago
from . import services


def _simular_cobro(card_number, cvv, expiration_date, total):
    """
    Simulación de cobro. En producción real aquí iría la integración
    con Stripe, Conekta, etc.
    Regla simple: si el número de tarjeta termina en '0000' → falla.
    """
    if card_number.replace(' ', '').endswith('0000'):
        return False
    return True


@extend_schema(
    request=ProcesarPagoSerializer,
    responses={200: PagoResponseSerializer, 402: None, 503: None}
)
class ProcesarPagoView(APIView):

    def post(self, request):
        serializer = ProcesarPagoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data     = serializer.validated_data
        order_id = data['order_id']
        user_id  = data['user_id']

        # 1. Consultar pedido a Equipo 3
        pedido = services.obtener_pedido(order_id)
        if pedido is None:
            return Response(
                {'error': 'El servicio de pedidos no responde. Intente más tarde.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # 3. Verificar que el pedido está pendiente
        if pedido.get('estado') != 'Pendiente':
            return Response(
                {'error': f"El pedido tiene estado '{pedido.get('estado')}'. Solo se pueden pagar pedidos 'Pendiente'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        total = pedido.get('total')

        # 4. Simular cobro con los datos de tarjeta
        cobro_exitoso = _simular_cobro(
            card_number     = data['card_number'],
            cvv             = data['cvv'],
            expiration_date = data['expiration_date'],
            total           = total
        )

        # 5. Guardar registro del pago (exitoso o fallido)
        pago = Pago.objects.create(
            order_id        = order_id,
            user_id         = user_id,
            total_cobrado   = total,
            card_number     = data['card_number'][-4:],   # solo últimos 4 dígitos
            expiration_date = data['expiration_date'],
            estado          = 'exitoso' if cobro_exitoso else 'fallido'
        )

        if not cobro_exitoso:
            return Response(
                {'error': 'El cobro fue rechazado. Verifique los datos de su tarjeta.'},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )

        # 6. Notificar a Equipo 3 que el pedido fue pagado
        notificado = services.marcar_pedido_pagado(order_id)
        if not notificado:
            # El pago se procesó pero no se pudo actualizar el pedido
            # Se guarda el pago y se devuelve advertencia
            return Response({
                'advertencia': 'Pago procesado pero no se pudo actualizar el estado del pedido.',
                'pago': PagoResponseSerializer(pago).data
            }, status=status.HTTP_207_MULTI_STATUS)

        return Response(
            PagoResponseSerializer(pago).data,
            status=status.HTTP_200_OK
        )