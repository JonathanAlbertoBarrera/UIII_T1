from rest_framework import serializers

from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    precio = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
    )
    stock = serializers.IntegerField(min_value=0, max_value=100000)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'fecha_registro']
        read_only_fields = ['id', 'fecha_registro']
        swagger_schema_fields = {
            'example': {
                'nombre': 'Coca Cola',
                'descripcion': 'Bebida de 600 ml',
                'precio': 19.50,
                'stock': 24,
            }
        }


class ReduceStockItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    cantidad = serializers.IntegerField(min_value=1)


class ReduceStockRequestSerializer(serializers.Serializer):
    items = ReduceStockItemSerializer(many=True)

    class Meta:
        swagger_schema_fields = {
            'example': {
                'items': [
                    {'id': 1, 'cantidad': 2},
                    {'id': 3, 'cantidad': 1},
                ]
            }
        }
