from django.db import models

class Pago(models.Model):
    ESTADO_CHOICES = [
        ('exitoso', 'Exitoso'),
        ('fallido', 'Fallido'),
    ]

    order_id        = models.IntegerField()
    user_id         = models.IntegerField()
    total_cobrado   = models.DecimalField(max_digits=10, decimal_places=2)
    card_number     = models.CharField(max_length=4)   # solo últimos 4 dígitos
    expiration_date = models.CharField(max_length=7)   # MM/YY
    estado          = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    fecha           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago #{self.id} — Pedido {self.order_id} — {self.estado}"