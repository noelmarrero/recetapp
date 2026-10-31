var formularioRegistro = document.getElementById("formulario-registro");
var mostrarContrasenas = document.getElementById("mostrar-contrasena");

var expresionCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

formularioRegistro.addEventListener("submit", function(evento) {
    evento.preventDefault();

    var nombre = document.getElementById("nombre");
    var apellido = document.getElementById("apellido");
    var correo = document.getElementById("correo");
    var usuario = document.getElementById("usuario");
    var contrasena = document.getElementById("contrasena");
    var repetirContrasena =
        document.getElementById("repetir-contrasena");

    var formularioValido = true;

    document.getElementById("error-nombre").textContent = "";
    document.getElementById("error-apellido").textContent = "";
    document.getElementById("error-correo").textContent = "";
    document.getElementById("error-usuario").textContent = "";
    document.getElementById("error-contrasena").textContent = "";
    document.getElementById("error-repetir").textContent = "";

    nombre.classList.remove("campo-error");
    apellido.classList.remove("campo-error");
    correo.classList.remove("campo-error");
    usuario.classList.remove("campo-error");
    contrasena.classList.remove("campo-error");
    repetirContrasena.classList.remove("campo-error");

    if (nombre.value.trim() === "") {
        document.getElementById("error-nombre").textContent =
            "Ingresá tu nombre.";

        nombre.classList.add("campo-error");
        formularioValido = false;
    }

    if (apellido.value.trim() === "") {
        document.getElementById("error-apellido").textContent =
            "Ingresá tu apellido.";

        apellido.classList.add("campo-error");
        formularioValido = false;
    }

    if (correo.value.trim() === "") {
        document.getElementById("error-correo").textContent =
            "Ingresá tu correo electrónico.";

        correo.classList.add("campo-error");
        formularioValido = false;
    } else if (!expresionCorreo.test(correo.value.trim())) {
        document.getElementById("error-correo").textContent =
            "Ingresá un correo válido.";

        correo.classList.add("campo-error");
        formularioValido = false;
    }

    if (usuario.value.trim() === "") {
        document.getElementById("error-usuario").textContent =
            "Elegí un nombre de usuario.";

        usuario.classList.add("campo-error");
        formularioValido = false;
    }

    if (contrasena.value.length < 6) {
        document.getElementById("error-contrasena").textContent =
            "Usá al menos 6 caracteres.";

        contrasena.classList.add("campo-error");
        formularioValido = false;
    }

    if (repetirContrasena.value === "") {
        document.getElementById("error-repetir").textContent =
            "Repetí la contraseña.";

        repetirContrasena.classList.add("campo-error");
        formularioValido = false;
    } else if (contrasena.value !== repetirContrasena.value) {
        document.getElementById("error-repetir").textContent =
            "Las contraseñas no coinciden.";

        repetirContrasena.classList.add("campo-error");
        formularioValido = false;
    }

    if (formularioValido === true) {
        alert("Cuenta creada correctamente.");
        window.location.href = "iniciar-sesion.html";
    }
});

mostrarContrasenas.addEventListener("change", function() {
    var contrasena = document.getElementById("contrasena");
    var repetirContrasena =
        document.getElementById("repetir-contrasena");

    if (mostrarContrasenas.checked === true) {
        contrasena.type = "text";
        repetirContrasena.type = "text";
    } else {
        contrasena.type = "password";
        repetirContrasena.type = "password";
    }
});