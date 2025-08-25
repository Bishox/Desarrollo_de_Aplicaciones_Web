import sqlite3

# Paso 1: Definir la clase Producto
# Esta clase representa un artículo individual en el inventario.
# Contiene los atributos básicos y métodos para acceder y modificar sus valores.
class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        """
        Constructor de la clase Producto.

        Args:
            id (int): Identificador único del producto.
            nombre (str): Nombre del producto.
            cantidad (int): Cantidad disponible en el inventario.
            precio (float): Precio de venta del producto.
        """
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # Métodos 'get' para acceder a los atributos
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # Métodos 'set' para modificar los atributos
    def set_cantidad(self, nueva_cantidad):
        self._cantidad = nueva_cantidad

    def set_precio(self, nuevo_precio):
        self._precio = nuevo_precio

    def __str__(self):
        return f"ID: {self._id}, Nombre: {self._nombre}, Cantidad: {self._cantidad}, Precio: ${self._precio:.2f}"

# -----------------------------------------------------------------------------

# Paso 2: Definir la clase Inventario
# Esta clase gestiona la colección de productos y la conexión con la base de datos SQLite.
class Inventario:
    def __init__(self, db_path='inventario.db'):
        """
        Constructor de la clase Inventario.

        Args:
            db_path (str): Ruta al archivo de la base de datos SQLite.
        """
        # Usamos un diccionario para un acceso rápido a los productos por ID.
        self.productos = {}
        self.db_path = db_path
        self._conectar_db()
        self._crear_tabla()
        self._cargar_productos()

    def _conectar_db(self):
        """Establece la conexión a la base de datos SQLite."""
        try:
            self.conexion = sqlite3.connect(self.db_path)
            self.cursor = self.conexion.cursor()
            print("Conexión a la base de datos exitosa.")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def _crear_tabla(self):
        """Crea la tabla 'productos' si no existe."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        self.conexion.commit()

    def _cargar_productos(self):
        """Carga los productos desde la base de datos al diccionario en memoria."""
        try:
            self.cursor.execute("SELECT id, nombre, cantidad, precio FROM productos")
            filas = self.cursor.fetchall()
            for fila in filas:
                producto = Producto(fila[0], fila[1], fila[2], fila[3])
                self.productos[producto.get_id()] = producto
            print(f"Se cargaron {len(self.productos)} productos desde la base de datos.")
        except sqlite3.Error as e:
            print(f"Error al cargar productos: {e}")

    # --- Operaciones CRUD ---

    def anadir_producto(self, producto):
        """
        Añade un nuevo producto al inventario y a la base de datos.
        
        Args:
            producto (Producto): El objeto Producto a añadir.
        """
        if producto.get_id() in self.productos:
            print("Error: Ya existe un producto con este ID.")
            return

        try:
            self.cursor.execute("INSERT INTO productos VALUES (?, ?, ?, ?)",
                                (producto.get_id(), producto.get_nombre(), producto.get_cantidad(), producto.get_precio()))
            self.conexion.commit()
            self.productos[producto.get_id()] = producto
            print(f"Producto '{producto.get_nombre()}' añadido con éxito.")
        except sqlite3.Error as e:
            print(f"Error al añadir el producto: {e}")

    def eliminar_producto(self, id):
        """
        Elimina un producto del inventario y la base de datos por su ID.
        
        Args:
            id (int): ID del producto a eliminar.
        """
        if id not in self.productos:
            print(f"Error: No se encontró un producto con ID {id}.")
            return

        try:
            self.cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
            self.conexion.commit()
            del self.productos[id]
            print(f"Producto con ID {id} eliminado con éxito.")
        except sqlite3.Error as e:
            print(f"Error al eliminar el producto: {e}")

    def actualizar_producto(self, id, nueva_cantidad=None, nuevo_precio=None):
        """
        Actualiza la cantidad o el precio de un producto.
        
        Args:
            id (int): ID del producto a actualizar.
            nueva_cantidad (int, opcional): La nueva cantidad.
            nuevo_precio (float, opcional): El nuevo precio.
        """
        if id not in self.productos:
            print(f"Error: No se encontró un producto con ID {id}.")
            return

        producto = self.productos[id]
        if nueva_cantidad is not None:
            producto.set_cantidad(nueva_cantidad)
        if nuevo_precio is not None:
            producto.set_precio(nuevo_precio)
        
        try:
            self.cursor.execute("UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?",
                                (producto.get_cantidad(), producto.get_precio(), id))
            self.conexion.commit()
            print(f"Producto con ID {id} actualizado con éxito.")
        except sqlite3.Error as e:
            print(f"Error al actualizar el producto: {e}")

    def buscar_producto_por_nombre(self, nombre):
        """
        Busca productos por nombre (búsqueda parcial).
        
        Args:
            nombre (str): El nombre o parte del nombre a buscar.
        """
        resultados = [p for p in self.productos.values() if nombre.lower() in p.get_nombre().lower()]
        if not resultados:
            print(f"No se encontraron productos con el nombre '{nombre}'.")
        else:
            print("\n--- Resultados de la Búsqueda ---")
            for producto in resultados:
                print(producto)

    def mostrar_todos_los_productos(self):
        """Muestra todos los productos en el inventario."""
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("\n--- Inventario Completo ---")
            for producto in self.productos.values():
                print(producto)

# -----------------------------------------------------------------------------

# Paso 3: Crear la interfaz de usuario en la consola.
def menu_principal():
    """Función principal que ejecuta la interfaz de usuario del sistema."""
    inventario = Inventario()

    while True:
        print("\n--- Sistema de Gestión de Inventario (Ferretería) ---")
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar cantidad/precio de un producto")
        print("4. Buscar productos por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            try:
                id = int(input("Ingrese el ID del producto: "))
                nombre = input("Ingrese el nombre del producto: ")
                cantidad = int(input("Ingrese la cantidad: "))
                precio = float(input("Ingrese el precio: "))
                nuevo_producto = Producto(id, nombre, cantidad, precio)
                inventario.anadir_producto(nuevo_producto)
            except ValueError:
                print("Entrada inválida. Asegúrese de ingresar números para ID, cantidad y precio.")

        elif opcion == '2':
            try:
                id = int(input("Ingrese el ID del producto a eliminar: "))
                inventario.eliminar_producto(id)
            except ValueError:
                print("Entrada inválida. El ID debe ser un número.")

        elif opcion == '3':
            try:
                id = int(input("Ingrese el ID del producto a actualizar: "))
                cantidad = input("Ingrese la nueva cantidad (deje en blanco para no cambiar): ")
                precio = input("Ingrese el nuevo precio (deje en blanco para no cambiar): ")
                
                nueva_cantidad = int(cantidad) if cantidad else None
                nuevo_precio = float(precio) if precio else None
                
                inventario.actualizar_producto(id, nueva_cantidad, nuevo_precio)
            except ValueError:
                print("Entrada inválida. La cantidad y el precio deben ser números.")

        elif opcion == '4':
            nombre = input("Ingrese el nombre (o parte del nombre) a buscar: ")
            inventario.buscar_producto_por_nombre(nombre)

        elif opcion == '5':
            inventario.mostrar_todos_los_productos()

        elif opcion == '6':
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    menu_principal()