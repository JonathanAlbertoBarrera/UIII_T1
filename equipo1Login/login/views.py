from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    MiTokenObtainPairSerializer,
    PerfilUsuarioSerializer,
    RegistroSerializer,
)

User = get_user_model()


class RegistroView(generics.CreateAPIView):
    """Registrar nuevos usuarios."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistroSerializer


class MiTokenObtainPairView(TokenObtainPairView):
    """Login usando email y JWT."""

    serializer_class = MiTokenObtainPairSerializer


class PerfilUsuarioView(generics.RetrieveAPIView):
    """Obtener datos del usuario (nombre, correo, dirección de envío)."""

    permission_classes = (IsAuthenticated,)
    serializer_class = PerfilUsuarioSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        usuario = get_object_or_404(User, pk=pk)
        solicitante = self.request.user
        if solicitante.is_staff or solicitante.pk == usuario.pk:
            return usuario
        raise PermissionDenied("No puedes ver el perfil de otro usuario.")
