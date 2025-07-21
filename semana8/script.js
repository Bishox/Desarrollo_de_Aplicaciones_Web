// Alerta personalizada
function mostrarAlerta() {
  alert("¡Gracias por visitar nuestra página interactiva!");
}

// Validación del formulario
document.getElementById("contactForm").addEventListener("submit", function (e) {
  e.preventDefault();

  let valido = true;

  const nombre = document.getElementById("nombre");
  const correo = document.getElementById("correo");
  const mensaje = document.getElementById("mensaje");

  // Validar nombre
  if (nombre.value.trim() === "") {
    nombre.classList.add("is-invalid");
    valido = false;
  } else {
    nombre.classList.remove("is-invalid");
  }

  // Validar correo
  const correoRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!correoRegex.test(correo.value.trim())) {
    correo.classList.add("is-invalid");
    valido = false;
  } else {
    correo.classList.remove("is-invalid");
  }

  // Validar mensaje
  if (mensaje.value.trim() === "") {
    mensaje.classList.add("is-invalid");
    valido = false;
  } else {
    mensaje.classList.remove("is-invalid");
  }

  if (valido) {
    alert("Formulario enviado correctamente. ¡Gracias!");
    // Aquí podrías limpiar el formulario o enviarlo a un servidor
    nombre.value = "";
    correo.value = "";
    mensaje.value = "";
  }
});
