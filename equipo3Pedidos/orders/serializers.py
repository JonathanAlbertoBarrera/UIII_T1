import requests
from decouple import config
from rest_framework import serializers

from .models import Order

EQ1_URL = config('EQ1_URL', default='http://127.0.0.1:8000')
EQ2_URL = config('EQ2_URL', default='http://127.0.0.1:8001')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'usuario_id', 'estado', 'productos', 'total', 'fecha']
        read_only_fields = ['id', 'fecha', 'total', 'productos', 'usuario_id']


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Solo permite actualizar el estado del pedido (usado por Equipo 4 y Equipo 5)."""
    ESTADOS_VALIDOS = ['Pendiente', 'Pagado', 'Enviado']

    class Meta:
        model = Order
        fields = ['estado']

    def validate_estado(self, value):
        if value not in self.ESTADOS_VALIDOS:
            raise serializers.ValidationError(
                f"Estado inválido. Opciones: {self.ESTADOS_VALIDOS}"
            )
        return value


class OrderCreateSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    productos  = serializers.ListField(
        child=serializers.DictField(), allow_empty=False
    )

    def validate(self, data):
        usuario_id      = data['usuario_id']
        productos_input = data['productos']

        # Reenviar JWT de Equipo 1 si lo manda el cliente
        request = self.context.get('request')
        auth_header = {}
        if request:
            token = request.headers.get('Authorization', '')
            if token:
                auth_header = {'Authorization': token}

        # 1. Validar usuario en Equipo 1
        try:
            r = requests.get(
                f"{EQ1_URL}/api/users/{usuario_id}/profile/",
                headers=auth_header,
                timeout=5,
            )
            if r.status_code == 404:
                raise serializers.ValidationError("Usuario no encontrado en Equipo 1.")
            if r.status_code == 401:
                raise serializers.ValidationError(
                    "Token inválido o expirado. Incluye el JWT de Equipo 1 en el header Authorization."
                )
            r.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise serializers.ValidationError(
                "Servicio de usuarios no disponible (Equipo 1)."
            )
        except requests.exceptions.Timeout:
            raise serializers.ValidationError(
                "Timeout al conectar con el servicio de usuarios (Equipo 1)."
            )

        # 2. Validar stock y obtener precios desde Equipo 2
        productos_detalle = []
        for item in productos_input:
            prod_id  = item.get('id')
            cantidad = item.get('cantidad', 0)

            if not prod_id or cantidad <= 0:
                raise serializers.ValidationError(
                    "Producto inválido: se requiere 'id' y 'cantidad' > 0."
                )

            try:
                r = requests.get(f"{EQ2_URL}/api/products/{prod_id}/", timeout=5)
                if r.status_code == 404:
                    raise serializers.ValidationError(
                        f"Producto {prod_id} no encontrado en catálogo (Equipo 2)."
                    )
                r.raise_for_status()
                prod_data = r.json()
            except requests.exceptions.ConnectionError:
                raise serializers.ValidationError(
                    "Servicio de catálogo no disponible (Equipo 2)."
                )
            except requests.exceptions.Timeout:
                raise serializers.ValidationError(
                    "Timeout al conectar con el servicio de catálogo (Equipo 2)."
                )

            stock_disponible = prod_data.get('stock', 0)
            if stock_disponible < cantidad:
                raise serializers.ValidationError(
                    f"Stock insuficiente para '{prod_data.get('nombre', prod_id)}'. "
                    f"Disponible: {stock_disponible}, solicitado: {cantidad}."
                )

            productos_detalle.append({
                'id':              prod_id,
                'nombre':          prod_data.get('nombre', ''),
                'cantidad':        cantidad,
                'precio_unitario': float(prod_data.get('precio', 0)),
            })

        data['_productos_detalle'] = productos_detalle
        return data

    def create(self, validated_data):
        usuario_id        = validated_data['usuario_id']
        productos_detalle = validated_data['_productos_detalle']

        # 3. Descontar stock en Equipo 2
        items_reducir = [
            {'id': p['id'], 'cantidad': p['cantidad']} for p in productos_detalle
        ]
        try:
            r = requests.post(
                f"{EQ2_URL}/api/products/reduce-stock/",
                json={'items': items_reducir},
                timeout=5,
            )
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise serializers.ValidationError(
                f"Error al descontar stock en Equipo 2: {str(e)}"
            )

        # 4. Calcular total y crear orden
        total = sum(p['cantidad'] * p['precio_unitario'] for p in productos_detalle)

        order = Order.objects.create(
            usuario_id=usuario_id,
            productos=productos_detalle,
            total=round(total, 2),
            estado='Pendiente',
        )
        return order

    def to_representation(self, instance):
        return OrderSerializer(instance).data
