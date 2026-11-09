# Reflexión — Proyecto Final POO

## 1. ¿Qué se refactorizó?

El Proyecto 1 utilizaba listas, diccionarios y funciones independientes. En esta versión la lógica se distribuyó entre clases con responsabilidades específicas.

`Producto` representa los datos y validaciones de cada artículo. `Inventario` administra la colección de productos. `Venta` representa una venta inmutable. `RepositorioCSV` maneja la persistencia, `Bitacora` registra operaciones y `ReporteVentas` genera el reporte diario. `SistemaInventario` coordina la interacción con el usuario.

## 2. Cuatro pilares de POO

**Encapsulamiento:** los atributos sensibles de `Producto` son privados y se modifican mediante propiedades y métodos como `descontar_stock()` y `reabastecer()`.

**Abstracción:** `ReglaNegocio` define el comportamiento general que deben implementar las reglas.

**Herencia:** `AlertaStock` y `AlertaStockCritico` heredan de `ReglaNegocio`.

**Polimorfismo:** `SistemaInventario` mantiene diferentes reglas y llama al mismo método `aplicar()` sobre ellas, sin preguntar qué tipo concreto de regla es.

## 3. Regla de negocio

La regla especial es la alerta de stock mínimo. Si `stock <= stock_minimo`, el producto necesita reabastecimiento.

Ejemplo: PlayStation 5 con stock 1 y mínimo 2 produce una alerta.

## 4. Estructuras de datos

- Diccionario interno de `Inventario`, usando el código como clave.
- `set` para las categorías.
- `dataclass(frozen=True)` para representar ventas inmutables.
- Listas para resultados de búsquedas, ordenamientos y alertas.

## 5. Archivos

El inventario y las ventas se almacenan en CSV. La bitácora utiliza modo append para conservar las operaciones anteriores.

## 6. Aprendizaje

La refactorización permitió separar responsabilidades y hacer que el sistema sea más fácil de mantener y explicar. Cada clase tiene una función concreta y los objetos colaboran para completar las operaciones del sistema.
