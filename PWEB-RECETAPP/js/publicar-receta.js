var formularioReceta = document.getElementById("formulario-receta");

formularioReceta.addEventListener("submit", function(evento) {
    evento.preventDefault();

    var nombre = document.getElementById("nombre-receta");
    var descripcion = document.getElementById("descripcion");
    var ingredientes = document.getElementById("ingredientes");
    var preparacion = document.getElementById("preparacion");
    var tiempo = document.getElementById("tiempo");
    var formularioValido = true;

    document.getElementById("error-nombre-receta").textContent = "";
    document.getElementById("error-descripcion").textContent = "";
    document.getElementById("error-ingredientes").textContent = "";
    document.getElementById("error-preparacion").textContent = "";
    document.getElementById("error-tiempo").textContent = "";

    nombre.classList.remove("campo-error");
    descripcion.classList.remove("campo-error");
    ingredientes.classList.remove("campo-error");
    preparacion.classList.remove("campo-error");
    tiempo.classList.remove("campo-error");

    if (nombre.value.trim() === "") {
        document.getElementById("error-nombre-receta").textContent = "Escribí el nombre de la receta.";
        nombre.classList.add("campo-error");
        formularioValido = false;
    }

    if (descripcion.value.trim() === "") {
        document.getElementById("error-descripcion").textContent = "Agregá una descripción.";
        descripcion.classList.add("campo-error");
        formularioValido = false;
    }

    if (ingredientes.value.trim() === "") {
        document.getElementById("error-ingredientes").textContent = "Agregá al menos un ingrediente.";
        ingredientes.classList.add("campo-error");
        formularioValido = false;
    }

    if (preparacion.value.trim() === "") {
        document.getElementById("error-preparacion").textContent = "Explicá cómo preparar la receta.";
        preparacion.classList.add("campo-error");
        formularioValido = false;
    }

    if (tiempo.value.trim() === "") {
        document.getElementById("error-tiempo").textContent = "Indicá el tiempo de preparación.";
        tiempo.classList.add("campo-error");
        formularioValido = false;
    }

    if (formularioValido === true) {
        alert("La receta fue enviada para revisión.");
        window.location.href = "perfil.html";
    }
});
