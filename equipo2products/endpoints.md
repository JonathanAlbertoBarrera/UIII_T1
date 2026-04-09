# Endpoints API Products

Base URL: http://localhost:8000/api/products/

---

## Listar todos (GET)
```cmd
curl http://localhost:8000/api/products/
```

---

## Ver uno (GET)
```cmd
curl http://localhost:8000/api/products/1/
```

---

## Crear product (POST)
```cmd
curl -X POST http://localhost:8000/api/products/ ^
  -H "Content-Type: application/json" ^
  -d "{\"nombre\":\"Laptop\",\"descripcion\":\"Laptop gaming\",\"precio\":15999.99,\"stock\":10}"
```

---

## Actualizar completo (PUT)
```cmd
curl -X PUT http://localhost:8000/api/products/1/ ^
  -H "Content-Type: application/json" ^
  -d "{\"nombre\":\"Laptop Pro\",\"descripcion\":\"Actualizada\",\"precio\":18999.99,\"stock\":5}"
```

---

## Actualizar parcial (PATCH)
```cmd
curl -X PATCH http://localhost:8000/api/products/1/ ^
  -H "Content-Type: application/json" ^
  -d "{\"precio\":16500.00}"
```

---

## Descontar stock masivo (POST)
Endpoint: `POST /api/products/reduce-stock/`

Recibe una lista de IDs y cantidades para descontar stock en una sola peticion.

```cmd
curl -X POST http://localhost:8000/api/products/reduce-stock/ ^
  -H "Content-Type: application/json" ^
  -d "{\"items\":[{\"id\":1,\"cantidad\":2},{\"id\":3,\"cantidad\":1}]}"
```

---

## Eliminar (DELETE)
```cmd
curl -X DELETE http://localhost:8000/api/products/1/
```
