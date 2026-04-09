from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MiUsuario


@admin.register(MiUsuario)
class MiUsuarioAdmin(UserAdmin):
    list_display = ("email", "nombre_completo", "direccion_envio", "telefono", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("email", "nombre_completo")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información Personal", {"fields": ("nombre_completo", "telefono")}),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Fechas Importantes", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nombre_completo", "password1", "password2", "direccion_envio", "telefono"),
        }),
    )
