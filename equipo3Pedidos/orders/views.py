from rest_framework import generics, status
from rest_framework.response import Response

from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer, OrderUpdateSerializer


class CreateOrderView(generics.CreateAPIView):
    """
    POST /api/orders/create/
    Crea un pedido. Recibe usuario_id y lista de productos.
    Requiere el JWT de Equipo 1 en el header Authorization.
    """
    serializer_class = OrderCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class OrderStatusView(generics.RetrieveAPIView):
    """
    GET /api/orders/<id>/status/
    Consulta el estado de un pedido (Pendiente, Pagado, Enviado).
    """
    queryset = Order.objects.all()

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        return Response({
            'id':     order.id,
            'estado': order.estado,
            'total':  order.total,
            'fecha':  order.fecha,
        })


class UpdateOrderView(generics.UpdateAPIView):
    """
    PATCH /api/orders/<id>/update/
    Actualiza el estado del pedido.
    Usado por Equipo 4 (Pagos) para marcar como 'Pagado'
    y Equipo 5 (Envíos) para marcar como 'Enviado'.
    """
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    http_method_names = ['patch', 'head', 'options']

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
