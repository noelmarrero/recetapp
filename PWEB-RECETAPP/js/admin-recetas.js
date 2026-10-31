var filtroRecetasAdmin = document.getElementById("filtro-receta");

filtroRecetasAdmin.addEventListener("change", function() {
    var recetas = document.getElementsByClassName("receta-admin");
    var categoriaElegida = filtroRecetasAdmin.value;
    var cantidadVisible = 0;

    for (var i = 0; i < recetas.length; i++) {
        var categoriaReceta = recetas[i].getAttribute("data-categoria");

        if (categoriaElegida === "todas" || categoriaElegida === categoriaReceta) {
            recetas[i].style.display = "";
            cantidadVisible = cantidadVisible + 1;
        } else {
            recetas[i].style.display = "none";
        }
    }

    if (cantidadVisible === 0) {
        document.getElementById("sin-recetas-admin").classList.remove("oculto");
    } else {
        document.getElementById("sin-recetas-admin").classList.add("oculto");
    }
});
