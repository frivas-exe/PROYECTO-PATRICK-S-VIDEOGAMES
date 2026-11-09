from datetime import datetime


class ReporteVentas:
    """Genera reportes de ventas con columnas alineadas."""

    def __init__(self, repositorio):
        self.__repositorio = repositorio

    def ventas_del_dia(self, fecha=None):
        """Retorna las ventas correspondientes a la fecha indicada."""
        fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        return [v for v in self.__repositorio.cargar_ventas() if v.fecha.startswith(fecha)]

    def mostrar(self):
        """Imprime el reporte de ventas del día y sus totales."""
        ventas = self.ventas_del_dia()
        print("\n" + "=" * 100)
        print("              REPORTE DE VENTAS DEL DIA")
        print("=" * 100)
        print(
            f"{'FECHA':<20} {'CODIGO':<10} {'PRODUCTO':<25}"
            f"{'CANTIDAD':>8} {'PRECIO':>13} {'TOTAL':>13}"
        )
        print("-" * 100)

        total = 0.0
        unidades = 0
        for venta in ventas:
            print(
                f"{venta.fecha:<20} {venta.codigo:<10} {venta.nombre:<25}"
                f"{venta.cantidad:>8} Q{venta.precio_unitario:>11,.2f}"
                f" Q{venta.total:>11,.2f}"
            )
            total += venta.total
            unidades += venta.cantidad

        print("-" * 100)
        if not ventas:
            print("No hay ventas registradas durante el día.")
        else:
            print(f"Cantidad de ventas: {len(ventas)}")
            print(f"Unidades vendidas: {unidades}")
            print(f"Total recaudado: Q{total:,.2f}")
        print("=" * 100)
