var formularioBusqueda = document.getElementById("formulario-busqueda");
var campoBusqueda = document.getElementById("buscar-receta");
var filtroCategoria = document.getElementById("categoria");
var botonesFavoritos = document.getElementsByClassName("boton-guardar");

function filtrarRecetas() {
    var recetas = document.getElementsByClassName("receta");
    var categoriaElegida = filtroCategoria.value;
    var textoBuscado = campoBusqueda.value.toLowerCase().trim();
    var cantidadVisible = 0;

    for (var i = 0; i < recetas.length; i++) {
        var categoriaReceta = recetas[i].getAttribute("data-categoria");
        var nombreReceta = recetas[i].getAttribute("data-nombre");
        var coincideCategoria = categoriaElegida === "todas" || categoriaElegida === categoriaReceta;
        var coincideNombre = nombreReceta.indexOf(textoBuscado) !== -1;

        if (coincideCategoria === true && coincideNombre === true) {
            recetas[i].style.display = "";
            cantidadVisible = cantidadVisible + 1;
        } else {
            recetas[i].style.display = "none";
        }
    }

    if (cantidadVisible === 0) {
        document.getElementById("sin-resultados").classList.remove("oculto");
    } else {
        document.getElementById("sin-resultados").classList.add("oculto");
    }
}

formularioBusqueda.addEventListener("submit", function(evento) {
    evento.preventDefault();
    filtrarRecetas();
});

filtroCategoria.addEventListener("change", function() {
    filtrarRecetas();
});

for (var i = 0; i < botonesFavoritos.length; i++) {
    botonesFavoritos[i].addEventListener("click", function() {
        if (this.textContent === "Agregar a favoritos") {
            this.textContent = "Agregada a favoritos";
        } else {
            this.textContent = "Agregar a favoritos";
        }
    });
}
