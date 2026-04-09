from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Obtiene dinámicamente tu modelo 'MiUsuario' gracias al settings.py
User = get_user_model()


class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "nombre_completo", "password", "direccion_envio", "telefono")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # create_user encripta el password vía el manager
        return User.objects.create_user(**validated_data)


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    """Datos públicos del perfil (sin contraseña)."""

    class Meta:
        model = User
        fields = ("id", "nombre_completo", "email", "direccion_envio")
        read_only_fields = fields


class MiTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer personalizado para login usando email."""

    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["nombre_completo"] = user.nombre_completo
        return token