from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="recetapp"
    )

    return conexion


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        mail = request.form["mail"]
        usuario = request.form["usuario"]
        contrasenia = request.form["contrasenia"]

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = """
            INSERT INTO usuario
            (nombre, apellido, mail, usuario, contrasenia)
            VALUES (%s, %s, %s, %s, %s)
        """

        datos = (
            nombre,
            apellido,
            mail,
            usuario,
            contrasenia
        )

        cursor.execute(consulta, datos)
        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/iniciar-sesion")

    return render_template("registrarse.html")


@app.route("/iniciar-sesion")
def iniciar_sesion():
    return render_template("iniciar-sesion.html")


if __name__ == "__main__":
    app.run(debug=True)