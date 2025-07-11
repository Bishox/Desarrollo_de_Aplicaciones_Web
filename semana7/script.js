// Arreglo inicial de productos
let productos = [
  { nombre: "Camiseta", precio: 15.99, descripcion: "Camiseta de algodón 100%" },
  { nombre: "Pantalón", precio: 29.99, descripcion: "Pantalón casual para diario" },
  { nombre: "Zapatos", precio: 49.99, descripcion: "Zapatos de cuero cómodos" }
];

// Función para renderizar la lista de productos
function renderizarProductos() {
  const lista = document.getElementById("lista-productos");
  lista.innerHTML = ""; // Limpiar contenido previo

  productos.forEach((producto) => {
    const item = document.createElement("li");
    item.innerHTML = `
      <strong>${producto.nombre}</strong><br>
      Precio: $${producto.precio.toFixed(2)}<br>
      <em>${producto.descripcion}</em>
    `;
    lista.appendChild(item);
  });
}

// Evento para agregar un nuevo producto
document.getElementById("agregar-producto").addEventListener("click", () => {
  const nuevoProducto = {
    nombre: "Producto Nuevo",
    precio: 9.99,
    descripcion: "Descripción genérica"
  };
  productos.push(nuevoProducto);
  renderizarProductos();
});

// Renderizar productos al cargar la página
document.addEventListener("DOMContentLoaded", renderizarProductos);
