var botonesQuitar = document.getElementsByClassName("quitar-favorito");

for (var i = botonesQuitar.length - 1; i >= 0; i--) {
    botonesQuitar[i].addEventListener("click", function() {
        var tarjetaFavorita = this.parentNode.parentNode;
        tarjetaFavorita.parentNode.removeChild(tarjetaFavorita);

        var favoritosRestantes = document.getElementsByClassName("favorito");

        if (favoritosRestantes.length === 0) {
            document.getElementById("favoritos-vacios").classList.remove("oculto");
        }
    });
}
