var formularioCategoria = document.getElementById("formulario-categoria");

formularioCategoria.addEventListener("submit", function(evento) {
    evento.preventDefault();

    var campoCategoria = document.getElementById("nueva-categoria");
    var errorCategoria = document.getElementById("error-categoria");

    errorCategoria.textContent = "";
    campoCategoria.classList.remove("campo-error");

    if (campoCategoria.value.trim() === "") {
        errorCategoria.textContent = "Escribí el nombre de la categoría.";
        campoCategoria.classList.add("campo-error");
    } else {
        formularioCategoria.submit();
    }
});
