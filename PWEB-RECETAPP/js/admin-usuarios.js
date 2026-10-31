var filtroUsuarios = document.getElementById("filtro-usuario");

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
