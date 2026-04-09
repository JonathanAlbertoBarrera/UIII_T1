from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class MiUsuarioManager(BaseUserManager):
    """Manager para crear usuarios y superusuarios con email como identificador."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Encripta la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class MiUsuario(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado que usa email para autenticación."""

    # Usaremos esto para el login
    email = models.EmailField(unique=True)
    nombre_completo = models.CharField(max_length=255)
    direccion_envio = models.TextField(blank=True, default="")
    telefono = models.CharField(max_length=20, blank=True, null=True)

    # Campos requeridos para compatibilidad con el admin de Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MiUsuarioManager()

    # Le decimos a Django que el login es con email
    USERNAME_FIELD = "email"
    # Campos extra al hacer createsuperuser
    REQUIRED_FIELDS = ["nombre_completo"]

    def __str__(self):
        return self.email