from django.urls import path

from .views import CreateOrderView, OrderStatusView, UpdateOrderView

urlpatterns = [
    path('orders/create/', CreateOrderView.as_view(), name='order-create'),
    path('orders/<int:pk>/status/', OrderStatusView.as_view(), name='order-status'),
    path('orders/<int:pk>/update/', UpdateOrderView.as_view(), name='order-update'),
]
