import os

import mysql.connector
from flask import Flask, flash, redirect, render_template, request, send_from_directory, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename


# Carpeta principal del proyecto.
CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, template_folder=CARPETA_PROYECTO, static_folder=None)
app.secret_key = "clave-recetapp"


# Estas rutas permiten usar las carpetas sin crear static.
@app.route("/css/<path:archivo>")
def cargar_css(archivo):
    return send_from_directory(os.path.join(CARPETA_PROYECTO, "css"), archivo)


@app.route("/js/<path:archivo>")
def cargar_js(archivo):
    return send_from_directory(os.path.join(CARPETA_PROYECTO, "js"), archivo)


@app.route("/imagenes/<path:archivo>")
def cargar_imagen(archivo):
    return send_from_directory(os.path.join(CARPETA_PROYECTO, "imagenes"), archivo)


# Abre la conexión con la base de datos de XAMPP.
def conectar_base():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="recetapp"
    )
    return conexion


# Página principal: consulta y muestra las recetas.
@app.route("/")
@app.route("/index.html")
def inicio():
    conexion = conectar_base()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categoria ORDER BY nombre")
    categorias = cursor.fetchall()

    cursor.execute("""
        SELECT receta.*, categoria.nombre AS categoria
        FROM receta
        INNER JOIN categoria
        ON receta.id_categoria = categoria.id
        WHERE receta.estado = 'disponible'
        ORDER BY receta.fechahora DESC
    """)
    recetas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "index.html",
        categorias=categorias,
        recetas=recetas
    )


# Registro de usuarios.
@app.route("/registrarse.html", methods=["GET", "POST"])
def registrarse():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        mail = request.form["mail"].strip()
        usuario = request.form["usuario"].strip()
        contrasenia = request.form["contrasenia"]

        conexion = conectar_base()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT id FROM usuario WHERE mail = %s OR usuario = %s",
            (mail, usuario)
        )
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            flash("El correo o el usuario ya están registrados.")
            cursor.close()
            conexion.close()
            return render_template("registrarse.html")

        contrasenia_segura = generate_password_hash(contrasenia)

        cursor.execute("""
            INSERT INTO usuario
            (nombre, apellido, mail, usuario, contrasenia, estado, rol)
            VALUES (%s, %s, %s, %s, %s, 'activo', 'usuario')
        """, (
            nombre,
            apellido,
            mail,
            usuario,
            contrasenia_segura
        ))

        conexion.commit()
        cursor.close()
        conexion.close()

        flash("Usuario registrado correctamente.")
        return redirect("/iniciar-sesion.html")

    return render_template("registrarse.html")


# Inicio de sesión.
@app.route("/iniciar-sesion.html", methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == "POST":
        mail = request.form["mail"].strip()
        contrasenia = request.form["contrasenia"]

        conexion = conectar_base()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM usuario WHERE mail = %s",
            (mail,)
        )
        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario is None:
            flash("El correo no está registrado.")
            return render_template("iniciar-sesion.html")

        if not check_password_hash(usuario["contrasenia"], contrasenia):
            flash("La contraseña es incorrecta.")
            return render_template("iniciar-sesion.html")

        if usuario["estado"] == "inactivo":
            flash("Este usuario está inactivo.")
            return render_template("iniciar-sesion.html")

        session["usuario_id"] = usuario["id"]
        session["usuario"] = usuario["usuario"]

        return redirect("/index.html")

    return render_template("iniciar-sesion.html")


# Elimina los datos guardados en la sesión.
@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.clear()
    return redirect("/index.html")


# Carga una nueva receta en la base de datos.
@app.route("/publicar-receta.html", methods=["GET", "POST"])
def publicar_receta():
    if "usuario_id" not in session:
        flash("Primero tenés que iniciar sesión.")
        return redirect("/iniciar-sesion.html")

    conexion = conectar_base()
    cursor = conexion.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        descripcion = request.form["descripcion"].strip()
        categoria = request.form["id_categoria"]
        ingredientes = request.form["ingredientes"].strip()
        preparacion = request.form["preparacion"].strip()
        tiempo = request.form["tiempo"]
        porciones = request.form["porciones"]
        dificultad = request.form["dificultad"]

        nombre_imagen = "logo-recetapp.png"
        imagen = request.files.get("imagen")

        if imagen and imagen.filename != "":
            nombre_imagen = secure_filename(imagen.filename)
            ruta_imagen = os.path.join(
                CARPETA_PROYECTO,
                "imagenes",
                nombre_imagen
            )
            imagen.save(ruta_imagen)

        cursor.execute("""
            INSERT INTO receta
            (id_usuario, id_categoria, nombre, descripcion,
             ingredientes, preparacion, tiempo, porciones,
             dificultad, estado, imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                    %s, 'disponible', %s)
        """, (
            session["usuario_id"],
            categoria,
            nombre,
            descripcion,
            ingredientes,
            preparacion,
            tiempo,
            porciones,
            dificultad,
            nombre_imagen
        ))

        conexion.commit()
        cursor.close()
        conexion.close()

        flash("La receta se cargó correctamente.")
        return redirect("/index.html")

    cursor.execute("SELECT * FROM categoria ORDER BY nombre")
    categorias = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "publicar-receta.html",
        categorias=categorias
    )


if __name__ == "__main__":
    app.run(debug=True)
