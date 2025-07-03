const form = document.getElementById("registroForm");
const btnEnviar = document.getElementById("btnEnviar");

const nombre = document.getElementById("nombre");
const correo = document.getElementById("correo");
const contrasena = document.getElementById("contrasena");
const confirmar = document.getElementById("confirmar");
const edad = document.getElementById("edad");

const errores = document.querySelectorAll("small.error");

const reqs = {
  nombre: document.getElementById("req-nombre"),
  correo: document.getElementById("req-correo"),
  contrasena: document.getElementById("req-contrasena"),
  confirmar: document.getElementById("req-confirmar"),
  edad: document.getElementById("req-edad")
};

const correoRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const contrasenaRegex = /^(?=.*[0-9])(?=.*[\W_]).{8,}$/;

function validarFormulario() {
  let valido = true;

  // Nombre
  if (nombre.value.trim().length >= 3) {
    marcarValido(nombre, errores[0], reqs.nombre);
  } else {
    marcarInvalido(nombre, errores[0], reqs.nombre, "El nombre debe tener mínimo 3 caracteres.");
    valido = false;
  }

  // Correo
  if (correoRegex.test(correo.value)) {
    marcarValido(correo, errores[1], reqs.correo);
  } else {
    marcarInvalido(correo, errores[1], reqs.correo, "Correo electrónico inválido.");
    valido = false;
  }

  // Contraseña
  if (contrasenaRegex.test(contrasena.value)) {
    marcarValido(contrasena, errores[2], reqs.contrasena);
  } else {
    marcarInvalido(contrasena, errores[2], reqs.contrasena, "Mínimo 8 caracteres, un número y un símbolo.");
    valido = false;
  }

  // Confirmar contraseña
  if (confirmar.value === contrasena.value && confirmar.value !== "") {
    marcarValido(confirmar, errores[3], reqs.confirmar);
  } else {
    marcarInvalido(confirmar, errores[3], reqs.confirmar, "Las contraseñas no coinciden.");
    valido = false;
  }

  // Edad
  if (parseInt(edad.value) >= 18) {
    marcarValido(edad, errores[4], reqs.edad);
  } else {
    marcarInvalido(edad, errores[4], reqs.edad, "Debes tener al menos 18 años.");
    valido = false;
  }

  btnEnviar.disabled = !valido;
  return valido;
}

function marcarValido(input, error, requisito) {
  input.classList.add("valid");
  input.classList.remove("invalid");
  error.textContent = "";
  error.classList.remove("active");
  requisito.classList.add("valido");
}

function marcarInvalido(input, error, requisito, mensaje) {
  input.classList.add("invalid");
  input.classList.remove("valid");
  error.textContent = mensaje;
  error.classList.add("active");
  requisito.classList.remove("valido");
}

// Eventos
[nombre, correo, contrasena, confirmar, edad].forEach(input => {
  input.addEventListener("input", validarFormulario);
});



console.log("JS cargado");


document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registroForm");
  const mensaje = document.getElementById("mensajeConfirmacion");
  const btnEnviar = document.getElementById("btnEnviar");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    // Mostrar mensaje
    mensaje.style.display = "flex";

    // Deshabilitar botón para evitar varios envíos
    btnEnviar.disabled = true;

    // Opcional: resetear formulario
    form.reset();

    // Ocultar mensaje después de 3 segundos
    setTimeout(() => {
      mensaje.style.display = "none";
      btnEnviar.disabled = false;
    }, 3000);
  });
});


