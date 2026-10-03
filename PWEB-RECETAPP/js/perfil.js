var estadosReceta = document.getElementsByClassName("estado-receta");
var mensajeEstado = document.getElementById("mensaje-estado");
var botonEditar = document.getElementById("editar-perfil");

for (var i = 0; i < estadosReceta.length; i++) {
    estadosReceta[i].addEventListener("change", function() {
        var nombreReceta = this.getAttribute("data-receta");
        mensajeEstado.textContent = "El estado de " + nombreReceta + " cambió a " + this.value + ".";
    });
}

botonEditar.addEventListener("click", function() {
    alert("La edición del perfil se agregará en una próxima entrega.");
});
