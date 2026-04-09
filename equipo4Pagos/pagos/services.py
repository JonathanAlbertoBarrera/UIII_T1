import os, requests
from django.conf import settings

ORDERS_URL = settings.ORDERS_SERVICE_URL
USE_MOCK = os.getenv('USE_MOCK_ORDERS', 'false').lower() == 'true'
def obtener_pedido(order_id):
    if USE_MOCK:
        from .mock_orders import mock_obtener_pedido
        return mock_obtener_pedido(order_id)
    """
    GET /api/orders/<id>/
    Retorna el dict del pedido o None si falla.
    """
    try:
        response = requests.get(
            f'{ORDERS_URL}/api/orders/{order_id}/status/',
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.HTTPError:
        return None
    except requests.exceptions.Timeout:
        return None


def marcar_pedido_pagado(order_id):
    if USE_MOCK:
        from .mock_orders import mock_marcar_pagado
        return mock_marcar_pagado(order_id)
    """
    PATCH /api/orders/<id>/status/
    Cambia el estado del pedido a 'Pagado'.
    """
    try:
        response = requests.patch(
            f'{ORDERS_URL}/api/orders/{order_id}/update/',
            json={'estado': 'Pagado'},
            timeout=5
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False