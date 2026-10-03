var botonGuardar = document.getElementById("boton-guardar");
var formularioComentario = document.getElementById("formulario-comentario");

botonGuardar.addEventListener("click", function() {
    if (botonGuardar.textContent === "Guardar receta") {
        botonGuardar.textContent = "Receta guardada";
    } else {
        botonGuardar.textContent = "Guardar receta";
    }
});

formularioComentario.addEventListener("submit", function(evento) {
    evento.preventDefault();

    var nombre = document.getElementById("nombre-comentario");
    var texto = document.getElementById("texto-comentario");
    var errorNombre = document.getElementById("error-nombre-comentario");
    var errorTexto = document.getElementById("error-texto-comentario");
    var formularioValido = true;

    errorNombre.textContent = "";
    errorTexto.textContent = "";
    nombre.classList.remove("campo-error");
    texto.classList.remove("campo-error");

    if (nombre.value.trim() === "") {
        errorNombre.textContent = "Ingresá tu nombre.";
        nombre.classList.add("campo-error");
        formularioValido = false;
    }

    if (texto.value.trim() === "") {
        errorTexto.textContent = "Escribí un comentario.";
        texto.classList.add("campo-error");
        formularioValido = false;
    }

    if (formularioValido === true) {
        var comentario = document.createElement("article");
        var autor = document.createElement("h3");
        var contenido = document.createElement("p");

        comentario.className = "comentario";
        autor.textContent = nombre.value;
        contenido.textContent = texto.value;

        comentario.appendChild(autor);
        comentario.appendChild(contenido);
        document.getElementById("lista-comentarios").appendChild(comentario);

        nombre.value = "";
        texto.value = "";
        alert("Comentario publicado.");
    }
});
