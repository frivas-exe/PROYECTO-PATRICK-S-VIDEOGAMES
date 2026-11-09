# Patrick's VideoGames — Proyecto Final POO

Sistema de inventario y ventas desarrollado en Python para el Proyecto Final de Algoritmos UMG.

## Objetivo

Refactorizar el Proyecto 1 aplicando Programación Orientada a Objetos sin perder las funcionalidades originales.

## Funcionalidades

- Agregar productos.
- Buscar por código o nombre parcial.
- Registrar ventas con validación de stock.
- Mostrar inventario ordenado por nombre, precio o existencias.
- Reporte de ventas del día.
- Alerta de stock mínimo.
- Reabastecimiento.
- Persistencia en CSV.
- Bitácora con fecha y hora.
- Manejo de excepciones personalizadas.

## POO aplicada

- Encapsulamiento: atributos privados y propiedades.
- Abstracción: `ReglaNegocio` con `ABC`.
- Herencia: `AlertaStock` y `AlertaStockCritico`.
- Polimorfismo: ambas reglas implementan `aplicar(inventario)`.
- Composición: `SistemaInventario` utiliza repositorio, bitácora, inventario y reglas.
- Métodos especiales: `__str__`, `__repr__`, `__len__`, `__contains__`, `__iter__`.
- `@classmethod`: `Producto.desde_fila_csv`.
- `@staticmethod`: `Producto.validar_codigo`.
- Excepciones personalizadas.

## Ejecución

Desde la carpeta raíz:

```bash
python main.py
```

No se requieren librerías externas; se utiliza únicamente la biblioteca estándar de Python.

## Regla de negocio

La regla especial del Proyecto 1 es la **alerta de stock mínimo**. Un producto necesita reabastecimiento cuando su stock actual es menor o igual al stock mínimo configurado.

Ejemplo: si un producto tiene stock 2 y stock mínimo 3, el sistema lo muestra como producto que necesita reabastecimiento.
