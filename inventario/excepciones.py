class InventarioError(Exception):
    """Excepción base para los errores controlados del sistema."""


class ProductoNoEncontradoError(InventarioError):
    """Se lanza cuando no existe un producto solicitado."""


class StockInsuficienteError(InventarioError):
    """Se lanza cuando no hay suficientes unidades para una venta."""


class CodigoInvalidoError(InventarioError):
    """Se lanza cuando un código no cumple el formato VG0000."""


class ArchivoInventarioError(InventarioError):
    """Se lanza cuando existe un problema al leer o escribir archivos."""
