import csv
from datetime import datetime
from pathlib import Path
from .excepciones import ArchivoInventarioError
from .modelos import Producto, Venta


class RepositorioCSV:
    """Se encarga exclusivamente de leer y escribir datos CSV."""

    CAMPOS_INVENTARIO = (
        "codigo", "nombre", "categoria", "precio", "stock", "stock_minimo"
    )
    CAMPOS_VENTAS = (
        "fecha", "codigo", "nombre", "cantidad", "precio_unitario", "total"
    )

    def __init__(self, ruta_inventario, ruta_ventas):
        self.__ruta_inventario = Path(ruta_inventario)
        self.__ruta_ventas = Path(ruta_ventas)

    def cargar_inventario(self):
        """Carga productos desde CSV y crea el archivo si no existe."""
        if not self.__ruta_inventario.exists():
            self.guardar_inventario([])
            return []

        try:
            with self.__ruta_inventario.open("r", newline="", encoding="utf-8") as archivo:
                lector = csv.DictReader(archivo)
                if lector.fieldnames is None or not all(
                    campo in lector.fieldnames for campo in self.CAMPOS_INVENTARIO
                ):
                    raise ArchivoInventarioError("Encabezados de inventario inválidos.")
                return [Producto.desde_fila_csv(fila) for fila in lector]
        except (OSError, ValueError, KeyError) as error:
            raise ArchivoInventarioError(
                f"No se pudo leer el inventario: {error}"
            ) from error

    def guardar_inventario(self, productos):
        """Guarda productos en CSV."""
        try:
            self.__ruta_inventario.parent.mkdir(parents=True, exist_ok=True)
            with self.__ruta_inventario.open("w", newline="", encoding="utf-8") as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=self.CAMPOS_INVENTARIO)
                escritor.writeheader()
                for producto in productos:
                    escritor.writerow(producto.a_fila_csv())
        except OSError as error:
            raise ArchivoInventarioError(
                f"No se pudo guardar el inventario: {error}"
            ) from error

    def guardar_venta(self, venta):
        """Agrega una venta al historial CSV."""
        try:
            archivo_nuevo = (
                not self.__ruta_ventas.exists()
                or self.__ruta_ventas.stat().st_size == 0
            )
            self.__ruta_ventas.parent.mkdir(parents=True, exist_ok=True)
            with self.__ruta_ventas.open("a", newline="", encoding="utf-8") as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=self.CAMPOS_VENTAS)
                if archivo_nuevo:
                    escritor.writeheader()
                escritor.writerow(venta.a_fila_csv())
        except OSError as error:
            raise ArchivoInventarioError(
                f"No se pudo guardar la venta: {error}"
            ) from error

    def cargar_ventas(self):
        """Carga las ventas registradas y las devuelve como objetos inmutables."""
        if not self.__ruta_ventas.exists():
            return []
        try:
            with self.__ruta_ventas.open("r", newline="", encoding="utf-8-sig") as archivo:
                lector = csv.DictReader(archivo)
                return [
                    Venta(
                        fila["fecha"], fila["codigo"], fila["nombre"],
                        int(fila["cantidad"]), float(fila["precio_unitario"]),
                        float(fila["total"])
                    )
                    for fila in lector
                ]
        except (OSError, ValueError, KeyError) as error:
            raise ArchivoInventarioError(
                f"No se pudo leer el historial de ventas: {error}"
            ) from error


class Bitacora:
    """Registra las operaciones del sistema en modo append."""

    def __init__(self, ruta):
        self.__ruta = Path(ruta)

    def registrar(self, mensaje):
        """Escribe una operación con fecha y hora en la bitácora."""
        try:
            self.__ruta.parent.mkdir(parents=True, exist_ok=True)
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with self.__ruta.open("a", encoding="utf-8") as archivo:
                archivo.write(f"{fecha_hora} - {mensaje}\n")
        except OSError as error:
            raise ArchivoInventarioError(
                f"No se pudo escribir la bitácora: {error}"
            ) from error
