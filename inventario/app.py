from pathlib import Path
from .excepciones import (
    InventarioError,
    ArchivoInventarioError,
    CodigoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
)
from .inventario import Inventario
from .modelos import Producto
from .persistencia import RepositorioCSV, Bitacora
from .reglas import AlertaStock, AlertaStockCritico
from .reportes import ReporteVentas


class SistemaInventario:
    """Coordina la interfaz de consola y los objetos del sistema."""

    def __init__(self, ruta_inventario):
        ruta = Path(ruta_inventario)
        carpeta = ruta.parent
        self.__repositorio = RepositorioCSV(
            ruta,
            carpeta / "ventas.csv",
        )
        self.__bitacora = Bitacora(carpeta / "bitacora.txt")
        self.__inventario = Inventario()
        self.__reporte = ReporteVentas(self.__repositorio)
        self.__reglas = [AlertaStock(), AlertaStockCritico()]
        self.__cargar_datos()

    def __cargar_datos(self):
        """Carga el inventario desde el repositorio."""
        productos = self.__repositorio.cargar_inventario()
        for producto in productos:
            self.__inventario.agregar(producto)

    def ejecutar(self):
        """Ejecuta el menú principal hasta que el usuario decide salir."""
        while True:
            self.__mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()
            try:
                if opcion == "1":
                    self.__agregar_producto()
                elif opcion == "2":
                    self.__buscar_producto()
                elif opcion == "3":
                    self.__registrar_venta()
                elif opcion == "4":
                    self.__mostrar_inventario()
                elif opcion == "5":
                    self.__reporte.mostrar()
                elif opcion == "6":
                    self.__revisar_stock()
                elif opcion == "7":
                    self.__reabastecer()
                elif opcion == "8":
                    self.__guardar()
                    print("Gracias por usar Patrick's VideoGames.")
                    break
                else:
                    print("Opción no válida. Intente nuevamente.")
            except (InventarioError, ValueError) as error:
                print(f"Error: {error}")

    def __mostrar_menu(self):
        """Muestra las opciones del sistema."""
        print("\n========================================")
        print("       PATRICK'S VIDEOGAMES")
        print("    SISTEMA DE INVENTARIO Y VENTAS")
        print("========================================")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Registrar venta")
        print("4. Mostrar inventario")
        print("5. Reporte de ventas del día")
        print("6. Revisar stock mínimo")
        print("7. Reabastecer producto")
        print("8. Salir")
        print("=" * 40)

    def __agregar_producto(self):
        """Solicita datos, crea un Producto y lo agrega al inventario."""
        print("\n========== AGREGAR PRODUCTO ==========")
        codigo = input("Ingrese el código: ").strip().upper()
        nombre = input("Ingrese el nombre: ")
        categoria = input("Ingrese la categoría: ")
        precio = float(input("Ingrese el precio: Q").strip().replace(",", "."))
        stock = int(input("Ingrese las existencias iniciales: "))
        stock_minimo = int(input("Ingrese el stock mínimo: "))

        producto = Producto(
            codigo, nombre, categoria, precio, stock, stock_minimo
        )
        self.__inventario.agregar(producto)
        self.__guardar()
        self.__bitacora.registrar(
            f"Producto agregado: {producto.codigo} - {producto.nombre}"
        )
        print("Producto agregado correctamente.")

    def __buscar_producto(self):
        """Busca y muestra productos por código o nombre parcial."""
        termino = input("Ingrese código o nombre: ").strip()
        encontrados = self.__inventario.buscar(termino)
        if not encontrados:
            print("No se encontraron productos.")
            return
        self.__imprimir_productos(encontrados)

    def __registrar_venta(self):
        """Solicita una venta, valida stock y la persiste."""
        codigo = input("Ingrese el código del producto: ").strip().upper()
        cantidad = int(input("Ingrese la cantidad: "))
        venta = self.__inventario.vender(codigo, cantidad)
        self.__repositorio.guardar_venta(venta)
        self.__guardar()
        self.__bitacora.registrar(
            f"Venta registrada: {venta.codigo} - {venta.nombre} - "
            f"Cantidad: {venta.cantidad} - Total: Q{venta.total:.2f}"
        )
        print("\n========== VENTA REGISTRADA ==========")
        print(f"Producto: {venta.nombre}")
        print(f"Cantidad vendida: {venta.cantidad}")
        print(f"Precio unitario: Q{venta.precio_unitario:.2f}")
        print(f"Total: Q{venta.total:.2f}")
        print(f"Existencias restantes: {self.__inventario.obtener(codigo).stock}")

    def __mostrar_inventario(self):
        """Muestra el inventario usando uno de tres criterios de orden."""
        print("\n1. Ordenar por nombre")
        print("2. Ordenar por precio")
        print("3. Ordenar por existencias")
        opcion = input("Seleccione: ").strip()
        if opcion == "1":
            productos = self.__inventario.ordenar_por_nombre()
        elif opcion == "2":
            productos = self.__inventario.ordenar_por_precio()
        elif opcion == "3":
            productos = self.__inventario.ordenar_por_stock()
        else:
            print("Opción de ordenamiento no válida.")
            return
        self.__imprimir_productos(productos)
        self.__bitacora.registrar("Inventario consultado y ordenado")

    def __imprimir_productos(self, productos):
        """Imprime una lista de productos con columnas alineadas."""
        print("\n" + "=" * 85)
        print("                 INVENTARIO DE PATRICK'S VIDEOGAMES")
        print("=" * 85)
        print(
            f"{'CODIGO':<10}{'NOMBRE':<28}{'CATEGORIA':<18}"
            f"{'PRECIO':>12}{'STOCK':>9}"
        )
        print("-" * 85)
        for producto in productos:
            print(
                f"{producto.codigo:<10}{producto.nombre:<28}"
                f"{producto.categoria:<18}Q{producto.precio:>10,.2f}"
                f"{producto.stock:>9}"
            )
        print("=" * 85)

    def __revisar_stock(self):
        """Aplica todas las reglas de stock mediante polimorfismo."""
        resultados = []
        for regla in self.__reglas:
            resultados.append(regla.aplicar(self.__inventario))

        bajos = resultados[0]
        criticos = resultados[1]
        print("\n========== REVISION DE STOCK ==========")
        if not bajos:
            print("Todos los productos tienen existencias suficientes.")
        else:
            print("¡ALERTA! PRODUCTOS QUE NECESITAN REABASTECIMIENTO")
            print("-" * 80)
            print(f"{'CODIGO':<10}{'PRODUCTO':<28}{'STOCK':>10}{'MINIMO':>10}")
            for producto in bajos:
                print(
                    f"{producto.codigo:<10}{producto.nombre:<28}"
                    f"{producto.stock:>10}{producto.stock_minimo:>10}"
                )
            print("-" * 80)
            print(f"Productos que necesitan reabastecimiento: {len(bajos)}")
        if criticos:
            print("\nProductos con stock crítico (0 unidades):")
            for producto in criticos:
                print(f"- {producto.codigo}: {producto.nombre}")

    def __reabastecer(self):
        """Aumenta el stock de un producto."""
        codigo = input("Ingrese el código: ").strip().upper()
        cantidad = int(input("Ingrese las unidades a agregar: "))
        self.__inventario.reabastecer(codigo, cantidad)
        self.__guardar()
        self.__bitacora.registrar(
            f"Reabastecimiento: {codigo}, unidades agregadas: {cantidad}"
        )
        print("Existencias actualizadas correctamente.")

    def __guardar(self):
        """Persiste el inventario actual."""
        self.__repositorio.guardar_inventario(self.__inventario.todos())
