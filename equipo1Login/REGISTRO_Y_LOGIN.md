# Servicio de identidad y registro (`equipo1Login`)

Este documento describe el proyecto Django **equipo1Login**, orientado a gestionar **clientes** y la **autenticación** del sistema mediante una API REST.

## Rol del proyecto

El objetivo es actuar como **proveedor de datos de usuarios**: exponer operaciones de **registro**, **inicio de sesión con JWT** y **consulta de perfil**, para que otras aplicaciones (por ejemplo frontends o microservicios) consuman esta información de forma segura.

## Estructura relevante

| Ruta | Descripción |
|------|-------------|
| `app login` | Modelo de usuario personalizado, serializers, vistas y URLs de la API. |
| `equipo1Login/` | Configuración del proyecto (`settings.py`, `urls.py` raíz). |

La app **`login`** concentra la lógica de identidad. El nombre del proyecto Django es `equipo1Login`.

## Modelo de usuario (`MiUsuario`)

Se usa un modelo **`AbstractBaseUser`** personalizado con:

- **Identificador de login**: correo electrónico (`email` único), no nombre de usuario.
- **Nombre**: `nombre_completo`.
- **Contraseña**: almacenada de forma segura mediante `set_password` (hash) en el manager.
- **Dirección de envío**: `direccion_envio` (texto libre; puede ir vacío en el registro).
- **Teléfono**: opcional `telefono`.
- **Flags de Django**: `is_active`, `is_staff` (compatibles con el panel de administración).

El **manager** (`MiUsuarioManager`) implementa `create_user` y `create_superuser` normalizando el email y delegando el hash de la contraseña a Django.

## Endpoints de la API

Todas las rutas bajo el prefijo **`/api/users/`** (definido en `equipo1Login/urls.py`).

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/users/register/` | Registrar un nuevo cliente. |
| `POST` | `/api/users/login/` | Autenticar con email y contraseña; devuelve tokens JWT (`access`, `refresh`). |
| `GET` | `/api/users/<id>/profile/` | Obtener datos del usuario: **id**, **nombre_completo**, **email**, **direccion_envio**. Requiere JWT. |

### Registro (`POST /api/users/register/`)

- **Público** (no requiere token).
- Cuerpo típico (JSON): `email`, `nombre_completo`, `password`, opcionalmente `direccion_envio` y `telefono`.
- La contraseña **no** se guarda en texto plano: el serializer llama a `User.objects.create_user(...)`, que aplica el hash.

### Login (`POST /api/users/login/`)

- **Público**.
- Usa **Simple JWT** con un serializer personalizado que trata el campo **`email`** como identificador (no `username`).
- Cuerpo esperado: `email` y `password`.
- Respuesta incluye tokens; además, en el payload del token se añaden reclamaciones útiles con **`email`** y **`nombre_completo`** (configuración en el serializer de token).

### Perfil (`GET /api/users/<id>/profile/`)

- **Protegido**: cabecera `Authorization: Bearer <access_token>`.
- Devuelve solo datos de perfil (sin contraseña).
- **Reglas de acceso**: un usuario solo puede ver **su propio** perfil (`id` coincide con el usuario autenticado); los **staff** pueden consultar cualquier `id`.

## Configuración de seguridad (resumen)

- En `settings.py`, REST Framework usa **JWT** como autenticación por defecto.
- Las variables sensibles (clave secreta, base de datos, etc.) se cargan desde el entorno (por ejemplo `.env` con `python-decouple`), según la configuración del proyecto.

## Flujo resumido

1. **Registro** → se crea el registro en base de datos con contraseña hasheada.
2. **Login** → se validan credenciales y se emiten tokens JWT.
3. **Perfil** → el cliente envía el token y obtiene nombre, correo y dirección de envío del usuario indicado.

## Cómo ejecutar migraciones

Con el entorno Python activo y las variables de base de datos configuradas:

```bash
python manage.py migrate
```

Esto aplica las migraciones de la app `login` (incluida la creación del modelo `MiUsuario` y el campo de dirección de envío).

---

*Documentación generada para el equipo de identidad y registro; describe únicamente el comportamiento del proyecto **equipo1Login**.*
