from django.urls import path
from .views import ProcesarPagoView

urlpatterns = [
    path('process/', ProcesarPagoView.as_view(), name='procesar-pago'),
]