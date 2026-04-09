from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema

from .models import Producto
from .serializers import ProductoSerializer, ReduceStockRequestSerializer


class ProductoViewSet(viewsets.ModelViewSet):
	queryset = Producto.objects.all().order_by('-id')
	serializer_class = ProductoSerializer

	@swagger_auto_schema(
		method='post',
		request_body=ReduceStockRequestSerializer,
		operation_summary='Descontar stock masivo',
		operation_description='Recibe una lista de productos con id y cantidad para descontar stock en una sola operacion.',
	)
	@action(detail=False, methods=['post'], url_path='reduce-stock')
	def reduce_stock(self, request):
		items = request.data
		if isinstance(request.data, dict):
			items = request.data.get('items')

		if not isinstance(items, list) or not items:
			return Response(
				{
					'detail': 'Debes enviar una lista en "items" con "id" y "cantidad".'
				},
				status=status.HTTP_400_BAD_REQUEST,
			)

		requested = {}
		for idx, item in enumerate(items):
			if not isinstance(item, dict):
				return Response(
					{'detail': f'El elemento en la posicion {idx} no es un objeto valido.'},
					status=status.HTTP_400_BAD_REQUEST,
				)

			product_id = item.get('id')
			quantity = item.get('cantidad')

			try:
				product_id = int(product_id)
				quantity = int(quantity)
			except (TypeError, ValueError):
				return Response(
					{
						'detail': (
							f'El elemento en la posicion {idx} debe tener '
							'"id" y "cantidad" numericos.'
						)
					},
					status=status.HTTP_400_BAD_REQUEST,
				)

			if quantity <= 0:
				return Response(
					{'detail': f'La cantidad para el producto {product_id} debe ser mayor a 0.'},
					status=status.HTTP_400_BAD_REQUEST,
				)

			requested[product_id] = requested.get(product_id, 0) + quantity

		with transaction.atomic():
			products = {
				product.id: product
				for product in Producto.objects.select_for_update().filter(id__in=requested.keys())
			}

			missing_ids = [pid for pid in requested.keys() if pid not in products]
			if missing_ids:
				return Response(
					{
						'detail': 'Algunos productos no existen.',
						'ids_no_encontrados': sorted(missing_ids),
					},
					status=status.HTTP_404_NOT_FOUND,
				)

			insufficient = []
			for product_id, quantity in requested.items():
				product = products[product_id]
				if quantity > product.stock:
					insufficient.append(
						{
							'id': product_id,
							'stock_actual': product.stock,
							'cantidad_solicitada': quantity,
						}
					)

			if insufficient:
				return Response(
					{
						'detail': 'Stock insuficiente en uno o mas productos.',
						'errores': insufficient,
					},
					status=status.HTTP_400_BAD_REQUEST,
				)

			results = []
			for product_id, quantity in requested.items():
				product = products[product_id]
				product.stock -= quantity
				product.save(update_fields=['stock'])
				results.append(
					{
						'id': product.id,
						'cantidad_descontada': quantity,
						'stock_actual': product.stock,
					}
				)

		return Response(
			{
				'detail': 'Stock descontado correctamente.',
				'actualizados': results,
			},
			status=status.HTTP_200_OK,
		)