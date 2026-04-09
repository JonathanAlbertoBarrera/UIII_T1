from django.db import models


class Order(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Pagado',    'Pagado'),
        ('Enviado',   'Enviado'),
    ]
    usuario_id = models.IntegerField()
    estado     = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    productos  = models.JSONField(default=list)
    total      = models.FloatField(default=0)
    fecha      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - Usuario {self.usuario_id} - {self.estado}"
