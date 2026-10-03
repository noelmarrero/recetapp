var formularioCategoria = document.getElementById("formulario-categoria");
var botonesEliminar = document.getElementsByClassName("eliminar-categoria");

function prepararBotonEliminar(boton) {
    boton.addEventListener("click", function() {
        var categoria = this.parentNode;
        var nombreCategoria = categoria.getElementsByTagName("span")[0].textContent;
        categoria.parentNode.removeChild(categoria);
        document.getElementById("mensaje-categoria").textContent = "La categoría " + nombreCategoria + " fue eliminada.";
    });
}

for (var i = 0; i < botonesEliminar.length; i++) {
    prepararBotonEliminar(botonesEliminar[i]);
}

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
        var elementoLista = document.createElement("li");
        var nombre = document.createElement("span");
        var boton = document.createElement("button");

        nombre.textContent = campoCategoria.value;
        boton.textContent = "Eliminar";
        boton.type = "button";
        boton.className = "eliminar-categoria";

        elementoLista.appendChild(nombre);
        elementoLista.appendChild(boton);
        document.getElementById("lista-categorias").appendChild(elementoLista);
        prepararBotonEliminar(boton);

        document.getElementById("mensaje-categoria").textContent = "La categoría fue creada.";
        campoCategoria.value = "";
    }
});
