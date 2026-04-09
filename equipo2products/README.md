# Equipo2 Products - API REST

API REST construida con Django 4.2 y Django REST Framework para gestionar un catalogo de productos.

Incluye:
- CRUD de products
- Endpoint masivo para descontar stock
- Swagger para probar endpoints desde el navegador

## Requisitos previos

- Python 3.10 o superior
- MySQL 8 corriendo localmente
- pip

## 1. Entrar al proyecto

```bash
cd equipo2products
```

## 2. Crear y activar entorno virtual

```bash
python -m venv venv
```

Windows CMD:

```cmd
venv\Scripts\activate
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Configurar variables de entorno

Copia el archivo de ejemplo:

```cmd
copy .env.example .env
```

Edita `.env` con tus credenciales reales:

```env
SECRET_KEY=django-insecure-pon-tu-clave-aqui
DEBUG=True
DB_NAME=nombre_de_tu_bd
DB_USER=tu_usuario_mysql
DB_PASSWORD=tu_contrasena
DB_HOST=localhost
DB_PORT=3306
```

## 5. Crear la base de datos en MySQL

```sql
CREATE DATABASE api_producto;
```

## 6. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## 7. Levantar el servidor

```bash
python manage.py runserver
```

Base API: http://localhost:8000/api/

## Swagger

Con el servidor levantado, puedes probar los endpoints desde Swagger en:

- http://localhost:8000/swagger/

Tambien puedes consultar la version Redoc en:

- http://localhost:8000/redoc/

## Endpoints

| Metodo | URL | Descripcion |
|--------|-----|-------------|
| GET | /api/products/ | Listar todos los products |
| POST | /api/products/ | Crear un product |
| GET | /api/products/{id}/ | Ver un product |
| PUT | /api/products/{id}/ | Actualizar completo |
| PATCH | /api/products/{id}/ | Actualizar parcial |
| DELETE | /api/products/{id}/ | Eliminar |
| POST | /api/products/reduce-stock/ | Descontar stock de multiples products |

### Ejemplo - Crear product

```json
{
	"nombre": "Laptop",
	"descripcion": "Laptop gaming",
	"precio": 15999.99,
	"stock": 10
}
```

### Ejemplo - Reduce stock masivo

```json
{
	"items": [
		{"id": 1, "cantidad": 2},
		{"id": 3, "cantidad": 1}
	]
}
```

## Archivos importantes

| Archivo | Descripcion |
|---------|-------------|
| .env | Variables de entorno reales (no se sube a git) |
| .env.example | Plantilla de variables de entorno |
| equipo2products/settings.py | Configuracion principal de Django |
| products/views.py | Logica de endpoints de products |
| products/urls.py | Rutas del app products |

## Notas

- El endpoint reduce-stock valida existencia de productos y stock suficiente antes de aplicar cambios.
- Si un item falla (por ejemplo, stock insuficiente), no se descuentan cambios parciales.
