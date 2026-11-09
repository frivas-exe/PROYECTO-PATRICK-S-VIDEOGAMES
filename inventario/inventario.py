from .excepciones import ProductoNoEncontradoError
from .modelos import Producto, Venta


class Inventario:
    """Gestiona la colección de productos de Patrick's VideoGames."""

    def __init__(self, productos=None):
        self.__productos = {}
        for producto in productos or []:
            self.agregar(producto)

    def agregar(self, producto):
        """Agrega un producto y rechaza códigos duplicados."""
        if producto.codigo in self.__productos:
            raise ValueError(f"Ya existe el código {producto.codigo}.")
        self.__productos[producto.codigo] = producto

    def obtener(self, codigo):
        """Retorna un producto por código o lanza una excepción."""
        codigo = codigo.strip().upper()
        try:
            return self.__productos[codigo]
        except KeyError as error:
            raise ProductoNoEncontradoError(
                f"No existe el producto {codigo}."
            ) from error

    def buscar(self, termino):
        """Busca por código o coincidencia parcial del nombre."""
        termino = termino.strip().casefold()
        if not termino:
            return []
        return [
            producto for producto in self.__productos.values()
            if termino in producto.codigo.casefold()
            or termino in producto.nombre.casefold()
        ]

    def vender(self, codigo, cantidad):
        """Registra una venta, descuenta stock y retorna la venta."""
        producto = self.obtener(codigo)
        producto.descontar_stock(cantidad)
        return Venta.crear(producto, cantidad)

    def reabastecer(self, codigo, cantidad):
        """Aumenta las existencias de un producto."""
        producto = self.obtener(codigo)
        producto.reabastecer(cantidad)

    def ordenar_por_nombre(self):
        """Retorna productos ordenados alfabéticamente por nombre."""
        return sorted(self.__productos.values(), key=lambda p: p.nombre.casefold())

    def ordenar_por_precio(self):
        """Retorna productos ordenados por precio ascendente."""
        return sorted(self.__productos.values(), key=lambda p: p.precio)

    def ordenar_por_stock(self):
        """Retorna productos ordenados por stock ascendente."""
        return sorted(self.__productos.values(), key=lambda p: p.stock)

    def categorias(self):
        """Retorna un set con las categorías existentes."""
        return {producto.categoria for producto in self.__productos.values()}

    def productos_bajos(self):
        """Retorna los productos que necesitan reabastecimiento."""
        return [p for p in self.__productos.values() if p.necesita_reabastecer()]

    def todos(self):
        """Retorna una lista con todos los productos."""
        return list(self.__productos.values())

    def __len__(self):
        """Retorna la cantidad de productos."""
        return len(self.__productos)

    def __contains__(self, codigo):
        """Permite usar 'codigo in inventario'."""
        return codigo.strip().upper() in self.__productos

    def __iter__(self):
        """Permite recorrer directamente el inventario."""
        return iter(self.__productos.values())

    def __str__(self):
        """Devuelve un resumen del inventario."""
        return f"Inventario con {len(self)} productos."

    def __repr__(self):
        """Devuelve una representación técnica del inventario."""
        return f"Inventario(productos={len(self)})"
