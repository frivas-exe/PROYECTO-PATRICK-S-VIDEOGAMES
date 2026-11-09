from dataclasses import dataclass
from datetime import datetime
import re
from .excepciones import CodigoInvalidoError, StockInsuficienteError


class Producto:
    """Representa un producto del inventario y protege sus datos sensibles."""

    def __init__(self, codigo, nombre, categoria, precio, stock, stock_minimo):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.stock_minimo = stock_minimo

    @staticmethod
    def validar_codigo(codigo):
        """Valida un código con el formato VG seguido de cuatro dígitos."""
        return bool(re.fullmatch(r"VG\d{4}", codigo.strip().upper()))

    @classmethod
    def desde_fila_csv(cls, fila):
        """Crea un producto a partir de una fila de un archivo CSV."""
        return cls(
            fila["codigo"],
            fila["nombre"],
            fila["categoria"],
            float(fila["precio"]),
            int(fila["stock"]),
            int(fila["stock_minimo"]),
        )

    @property
    def codigo(self):
        """Retorna el código del producto."""
        return self.__codigo

    @codigo.setter
    def codigo(self, valor):
        """Valida y asigna el código del producto."""
        valor = str(valor).strip().upper()
        if not self.validar_codigo(valor):
            raise CodigoInvalidoError("El código debe tener el formato VG0000.")
        self.__codigo = valor

    @property
    def nombre(self):
        """Retorna el nombre normalizado."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        """Asigna un nombre no vacío y normalizado."""
        valor = " ".join(str(valor).strip().split())
        if not valor:
            raise ValueError("El nombre es obligatorio.")
        self.__nombre = valor

    @property
    def categoria(self):
        """Retorna la categoría."""
        return self.__categoria

    @categoria.setter
    def categoria(self, valor):
        """Asigna una categoría normalizada."""
        valor = " ".join(str(valor).strip().split()).title()
        if not valor:
            raise ValueError("La categoría es obligatoria.")
        self.__categoria = valor

    @property
    def precio(self):
        """Retorna el precio."""
        return self.__precio

    @precio.setter
    def precio(self, valor):
        """Valida y asigna un precio no negativo."""
        valor = float(valor)
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = round(valor, 2)

    @property
    def stock(self):
        """Retorna las existencias actuales."""
        return self.__stock

    @stock.setter
    def stock(self, valor):
        """Valida y asigna las existencias."""
        valor = int(valor)
        if valor < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.__stock = valor

    @property
    def stock_minimo(self):
        """Retorna el stock mínimo."""
        return self.__stock_minimo

    @stock_minimo.setter
    def stock_minimo(self, valor):
        """Valida y asigna el stock mínimo."""
        valor = int(valor)
        if valor < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")
        self.__stock_minimo = valor

    def descontar_stock(self, cantidad):
        """Descuenta unidades si existe stock suficiente."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if cantidad > self.__stock:
            raise StockInsuficienteError(
                f"Stock insuficiente. Disponible: {self.__stock}."
            )
        self.__stock -= cantidad

    def reabastecer(self, cantidad):
        """Aumenta el stock del producto."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        self.__stock += int(cantidad)

    def necesita_reabastecer(self):
        """Indica si el stock está en o por debajo del mínimo."""
        return self.__stock <= self.__stock_minimo

    def a_fila_csv(self):
        """Convierte el producto en un diccionario compatible con CSV."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
            "stock_minimo": self.stock_minimo,
        }

    def __str__(self):
        """Devuelve una representación legible del producto."""
        return f"{self.codigo} - {self.nombre} | Q{self.precio:,.2f} | Stock: {self.stock}"

    def __repr__(self):
        """Devuelve una representación técnica del producto."""
        return (
            f"Producto({self.codigo!r}, {self.nombre!r}, {self.categoria!r}, "
            f"{self.precio!r}, {self.stock!r}, {self.stock_minimo!r})"
        )


@dataclass(frozen=True)
class Venta:
    """Representa una venta inmutable."""

    fecha: str
    codigo: str
    nombre: str
    cantidad: int
    precio_unitario: float
    total: float

    @classmethod
    def crear(cls, producto, cantidad):
        """Crea una venta calculando su total a partir de un producto."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        return cls(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            producto.codigo,
            producto.nombre,
            cantidad,
            producto.precio,
            round(producto.precio * cantidad, 2),
        )

    def a_fila_csv(self):
        """Convierte la venta en una fila compatible con CSV."""
        return {
            "fecha": self.fecha,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "total": self.total,
        }

    def __str__(self):
        """Devuelve una descripción legible de la venta."""
        return f"{self.codigo} - {self.nombre} x{self.cantidad} = Q{self.total:,.2f}"

    def __repr__(self):
        """Devuelve una representación técnica de la venta."""
        return f"Venta({self.fecha!r}, {self.codigo!r}, {self.nombre!r}, {self.cantidad!r}, {self.precio_unitario!r}, {self.total!r})"
