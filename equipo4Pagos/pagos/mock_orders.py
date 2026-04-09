MOCK_ORDERS = {
    1: {'id': 1, 'user_id': 1, 'total': '250.00', 'status': 'Pendiente'},
    2: {'id': 2, 'user_id': 2, 'total': '89.99',  'status': 'Pendiente'},
}

def mock_obtener_pedido(order_id):
    return MOCK_ORDERS.get(order_id)

def mock_marcar_pagado(order_id):
    if order_id in MOCK_ORDERS:
        MOCK_ORDERS[order_id]['status'] = 'Pagado'
        return True
    return False