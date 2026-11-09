from abc import ABC, abstractmethod


class ReglaNegocio(ABC):
    """Define el contrato abstracto para las reglas de negocio."""

    @abstractmethod
    def aplicar(self, inventario):
        """Aplica la regla sobre el inventario y retorna un resultado."""
        raise NotImplementedError


class AlertaStock(ReglaNegocio):
    """Regla que detecta productos en o por debajo del stock mínimo."""

    def aplicar(self, inventario):
        """Retorna los productos que requieren reabastecimiento."""
        return inventario.productos_bajos()


class AlertaStockCritico(ReglaNegocio):
    """Regla que detecta productos con stock igual a cero."""

    def aplicar(self, inventario):
        """Retorna los productos cuyo stock llegó a cero."""
        return [producto for producto in inventario if producto.stock == 0]
