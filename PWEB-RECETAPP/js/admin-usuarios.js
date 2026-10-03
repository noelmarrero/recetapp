var filtroUsuarios = document.getElementById("filtro-usuario");
var estadosUsuario = document.getElementsByClassName("estado-usuario");

filtroUsuarios.addEventListener("change", function() {
    var usuarios = document.getElementsByClassName("usuario-admin");
    var opcionElegida = filtroUsuarios.value;

    for (var i = 0; i < usuarios.length; i++) {
        var publicoRecetas = usuarios[i].getAttribute("data-publico");

        if (opcionElegida === "todos" || opcionElegida === publicoRecetas) {
            usuarios[i].style.display = "";
        } else {
            usuarios[i].style.display = "none";
        }
    }
});

for (var i = 0; i < estadosUsuario.length; i++) {
    estadosUsuario[i].addEventListener("change", function() {
        var nombreUsuario = this.getAttribute("data-usuario");
        document.getElementById("mensaje-usuario").textContent = "La cuenta de " + nombreUsuario + " ahora está " + this.value.toLowerCase() + ".";
    });
}
