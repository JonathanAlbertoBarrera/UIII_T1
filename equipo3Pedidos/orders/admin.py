from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario_id', 'estado', 'total', 'fecha']
    list_filter  = ['estado']
