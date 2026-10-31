var formularioComentario = document.getElementById("formulario-comentario");

if (formularioComentario) {
    formularioComentario.addEventListener("submit", function(evento) {
        evento.preventDefault();

        var texto = document.getElementById("texto-comentario");
        var errorTexto = document.getElementById("error-texto-comentario");

        errorTexto.textContent = "";
        texto.classList.remove("campo-error");

        if (texto.value.trim() === "") {
            errorTexto.textContent = "Escribí un comentario.";
            texto.classList.add("campo-error");
        } else {
            formularioComentario.submit();
        }
    });
}
