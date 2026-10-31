var formularioLogin = document.getElementById("formulario-login");
var mostrarContrasena = document.getElementById("mostrar-contrasena");

var expresionCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

formularioLogin.addEventListener("submit", function(evento) {
    evento.preventDefault();

    var correo = document.getElementById("correo");
    var contrasena = document.getElementById("contrasena");

    var errorCorreo = document.getElementById("error-correo");
    var errorContrasena = document.getElementById("error-contrasena");

    var formularioValido = true;

    errorCorreo.textContent = "";
    errorContrasena.textContent = "";

    correo.classList.remove("campo-error");
    contrasena.classList.remove("campo-error");

    if (correo.value.trim() === "") {
        errorCorreo.textContent = "Ingresá tu correo electrónico.";
        correo.classList.add("campo-error");
        formularioValido = false;
    } else if (!expresionCorreo.test(correo.value.trim())) {
        errorCorreo.textContent = "Ingresá un correo válido.";
        correo.classList.add("campo-error");
        formularioValido = false;
    }

    if (contrasena.value === "") {
        errorContrasena.textContent = "Ingresá tu contraseña.";
        contrasena.classList.add("campo-error");
        formularioValido = false;
    } else if (contrasena.value.length < 6) {
        errorContrasena.textContent =
            "La contraseña debe tener al menos 6 caracteres.";

        contrasena.classList.add("campo-error");
        formularioValido = false;
    }

    if (formularioValido === true) {
        alert("Inicio de sesión correcto.");
        window.location.href = "perfil.html";
    }
});

mostrarContrasena.addEventListener("change", function() {
    var contrasena = document.getElementById("contrasena");

    if (mostrarContrasena.checked === true) {
        contrasena.type = "text";
    } else {
        contrasena.type = "password";
    }
});