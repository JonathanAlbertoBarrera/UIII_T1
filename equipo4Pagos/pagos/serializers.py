from rest_framework import serializers
from .models import Pago

class ProcesarPagoSerializer(serializers.Serializer):
    #Datos que recibe el endpoint para procesar un pago.
    order_id        = serializers.IntegerField()
    user_id         = serializers.IntegerField()
    card_number     = serializers.CharField(max_length=19)
    expiration_date = serializers.CharField(max_length=7)   # MM/YY
    cvv             = serializers.CharField(max_length=4, write_only=True)


class PagoResponseSerializer(serializers.ModelSerializer):
    #Datos que se devuelven tras procesar el pago.
    class Meta:
        model  = Pago
        fields = ['id', 'order_id', 'user_id', 'total_cobrado',
                  'card_number', 'estado', 'fecha']