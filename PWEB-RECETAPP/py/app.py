import os

import mysql.connector
from flask import Flask, flash, redirect, render_template, request, send_from_directory, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename


CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=CARPETA_PROYECTO,
    static_folder=None
)
app.secret_key = "recetapp-clave-de-desarrollo"


@app.route("/css/<path:archivo>")
def archivos_css(archivo):
    return send_from_directory(os.path.join(CARPETA_PROYECTO, "css"), archivo)


@app.route("/js/<path:archivo>")
def archivos_js(archivo):
    return send_from_directory(os.path.join(CARPETA_PROYECTO, "js"), archivo)


@app.route("/imagenes/<path:archivo>")
def archivos_imagenes(archivo):
    return send_from_directory(os.path.join(CARPETA_PROYECTO, "imagenes"), archivo)


def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="recetapp"
    )


def usuario_conectado():
    return "usuario_id" in session


def administrador_conectado():
    return session.get("rol") == "admin"


@app.route("/")
@app.route("/index.html")
def inicio():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categoria ORDER BY nombre")
    categorias = cursor.fetchall()

    cursor.execute("""
        SELECT receta.*, categoria.nombre AS categoria,
               usuario.usuario AS autor_usuario
        FROM receta
        INNER JOIN categoria ON receta.id_categoria = categoria.id
        INNER JOIN usuario ON receta.id_usuario = usuario.id
        WHERE receta.estado = 'disponible'
        ORDER BY receta.fechahora DESC
    """)
    recetas = cursor.fetchall()

    favoritos = []

    if usuario_conectado():
        cursor.execute(
            "SELECT id_receta FROM favorito WHERE id_usuario = %s",
            (session["usuario_id"],)
        )
        favoritos = [fila["id_receta"] for fila in cursor.fetchall()]

    cursor.close()
    conexion.close()

    return render_template(
        "index.html",
        recetas=recetas,
        categorias=categorias,
        favoritos=favoritos
    )


@app.route("/registrarse.html", methods=["GET", "POST"])
def registrarse():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        mail = request.form["mail"].strip()
        nombre_usuario = request.form["usuario"].strip()
        contrasenia = request.form["contrasenia"]

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT id FROM usuario WHERE mail = %s OR usuario = %s",
            (mail, nombre_usuario)
        )
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            flash("El correo o el nombre de usuario ya están registrados.")
            cursor.close()
            conexion.close()
            return render_template("registrarse.html")

        contrasenia_segura = generate_password_hash(contrasenia)

        cursor.execute("""
            INSERT INTO usuario
                (nombre, apellido, mail, usuario, contrasenia, estado, rol)
            VALUES
                (%s, %s, %s, %s, %s, 'activo', 'usuario')
        """, (
            nombre,
            apellido,
            mail,
            nombre_usuario,
            contrasenia_segura
        ))

        conexion.commit()
        cursor.close()
        conexion.close()

        flash("La cuenta fue creada. Ahora podés iniciar sesión.")
        return redirect("/iniciar-sesion.html")

    return render_template("registrarse.html")


@app.route("/iniciar-sesion.html", methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == "POST":
        mail = request.form["mail"].strip()
        contrasenia = request.form["contrasenia"]

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE mail = %s", (mail,))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()

        if usuario is None or not check_password_hash(usuario["contrasenia"], contrasenia):
            flash("El correo o la contraseña son incorrectos.")
            return render_template("iniciar-sesion.html")

        if usuario["estado"] == "inactivo":
            flash("Esta cuenta se encuentra inactiva.")
            return render_template("iniciar-sesion.html")

        session["usuario_id"] = usuario["id"]
        session["nombre"] = usuario["nombre"]
        session["usuario"] = usuario["usuario"]
        session["rol"] = usuario["rol"]

        if usuario["rol"] == "admin":
            return redirect("/admin.html")

        return redirect("/perfil.html")

    return render_template("iniciar-sesion.html")


@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.clear()
    return redirect("/index.html")


@app.route("/publicar-receta.html", methods=["GET", "POST"])
def publicar_receta():
    if not usuario_conectado():
        flash("Tenés que iniciar sesión para publicar una receta.")
        return redirect("/iniciar-sesion.html")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        id_categoria = request.form["id_categoria"]
        ingredientes = request.form["ingredientes"]
        preparacion = request.form["preparacion"]
        tiempo = request.form["tiempo"]
        porciones = request.form["porciones"]
        dificultad = request.form["dificultad"]
        imagen_nombre = "logo-recetapp.png"

        imagen = request.files.get("imagen")

        if imagen and imagen.filename != "":
            imagen_nombre = secure_filename(imagen.filename)
            ruta_imagen = os.path.join(CARPETA_PROYECTO, "imagenes", imagen_nombre)
            imagen.save(ruta_imagen)

        cursor.execute("""
            INSERT INTO receta
                (id_usuario, id_categoria, nombre, descripcion,
                 ingredientes, preparacion, tiempo, porciones,
                 dificultad, estado, imagen)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'en_revision', %s)
        """, (
            session["usuario_id"],
            id_categoria,
            nombre,
            descripcion,
            ingredientes,
            preparacion,
            tiempo,
            porciones,
            dificultad,
            imagen_nombre
        ))

        conexion.commit()
        cursor.close()
        conexion.close()

        flash("La receta fue enviada para revisión.")
        return redirect("/perfil.html")

    cursor.execute("SELECT * FROM categoria ORDER BY nombre")
    categorias = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template("publicar-receta.html", categorias=categorias)


@app.route("/receta.html")
def ver_receta():
    id_receta = request.args.get("id", type=int)

    if id_receta is None:
        return redirect("/index.html")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT receta.*, categoria.nombre AS categoria,
               usuario.id AS autor_id,
               usuario.nombre AS autor_nombre,
               usuario.apellido AS autor_apellido,
               usuario.usuario AS autor_usuario
        FROM receta
        INNER JOIN categoria ON receta.id_categoria = categoria.id
        INNER JOIN usuario ON receta.id_usuario = usuario.id
        WHERE receta.id = %s
    """, (id_receta,))
    receta = cursor.fetchone()

    if receta is None:
        cursor.close()
        conexion.close()
        return redirect("/index.html")

    cursor.execute("""
        SELECT comentario.*, usuario.nombre, usuario.apellido
        FROM comentario
        INNER JOIN usuario ON comentario.id_usuario = usuario.id
        WHERE comentario.id_receta = %s
        ORDER BY comentario.fechahora DESC
    """, (id_receta,))
    comentarios = cursor.fetchall()

    es_favorita = False

    if usuario_conectado():
        cursor.execute("""
            SELECT id FROM favorito
            WHERE id_usuario = %s AND id_receta = %s
        """, (session["usuario_id"], id_receta))
        es_favorita = cursor.fetchone() is not None

    cursor.close()
    conexion.close()

    return render_template(
        "receta.html",
        receta=receta,
        comentarios=comentarios,
        es_favorita=es_favorita
    )


@app.route("/comentar/<int:id_receta>", methods=["POST"])
def comentar(id_receta):
    if not usuario_conectado():
        flash("Tenés que iniciar sesión para comentar.")
        return redirect("/iniciar-sesion.html")

    contenido = request.form["contenido"].strip()

    if contenido != "":
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO comentario (id_usuario, id_receta, contenido)
            VALUES (%s, %s, %s)
        """, (session["usuario_id"], id_receta, contenido))
        conexion.commit()
        cursor.close()
        conexion.close()

    return redirect("/receta.html?id=" + str(id_receta))


@app.route("/favorito/<int:id_receta>", methods=["POST"])
def cambiar_favorito(id_receta):
    if not usuario_conectado():
        flash("Tenés que iniciar sesión para guardar favoritos.")
        return redirect("/iniciar-sesion.html")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id FROM favorito
        WHERE id_usuario = %s AND id_receta = %s
    """, (session["usuario_id"], id_receta))
    favorito = cursor.fetchone()

    if favorito:
        cursor.execute("DELETE FROM favorito WHERE id = %s", (favorito["id"],))
    else:
        cursor.execute("""
            INSERT INTO favorito (id_usuario, id_receta)
            VALUES (%s, %s)
        """, (session["usuario_id"], id_receta))

    conexion.commit()
    cursor.close()
    conexion.close()

    destino = request.form.get("destino", "/index.html")
    return redirect(destino)


@app.route("/favoritos.html")
def favoritos():
    if not usuario_conectado():
        flash("Tenés que iniciar sesión para ver tus favoritos.")
        return redirect("/iniciar-sesion.html")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT receta.*
        FROM favorito
        INNER JOIN receta ON favorito.id_receta = receta.id
        WHERE favorito.id_usuario = %s
        ORDER BY favorito.fechahora DESC
    """, (session["usuario_id"],))
    recetas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template("favoritos.html", recetas=recetas)


@app.route("/perfil.html")
def perfil():
    if not usuario_conectado():
        flash("Tenés que iniciar sesión para ver tu perfil.")
        return redirect("/iniciar-sesion.html")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE id = %s", (session["usuario_id"],))
    usuario = cursor.fetchone()
    cursor.execute("""
        SELECT * FROM receta
        WHERE id_usuario = %s
        ORDER BY fechahora DESC
    """, (session["usuario_id"],))
    recetas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template("perfil.html", usuario=usuario, recetas=recetas)


@app.route("/cambiar-estado-propio/<int:id_receta>", methods=["POST"])
def cambiar_estado_propio(id_receta):
    if not usuario_conectado():
        return redirect("/iniciar-sesion.html")

    estado = request.form["estado"]

    if estado in ["disponible", "no_disponible"]:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE receta SET estado = %s
            WHERE id = %s AND id_usuario = %s
        """, (estado, id_receta, session["usuario_id"]))
        conexion.commit()
        cursor.close()
        conexion.close()

    return redirect("/perfil.html")


@app.route("/perfil-publico.html")
def perfil_publico():
    id_usuario = request.args.get("id", type=int)

    if id_usuario is None:
        return redirect("/index.html")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE id = %s", (id_usuario,))
    usuario = cursor.fetchone()
    cursor.execute("""
        SELECT * FROM receta
        WHERE id_usuario = %s AND estado = 'disponible'
        ORDER BY fechahora DESC
    """, (id_usuario,))
    recetas = cursor.fetchall()
    cursor.close()
    conexion.close()

    if usuario is None:
        return redirect("/index.html")

    return render_template("perfil-publico.html", usuario=usuario, recetas=recetas)


@app.route("/admin.html")
def admin():
    if not administrador_conectado():
        return redirect("/iniciar-sesion.html")

    return render_template("admin.html")


@app.route("/admin-recetas.html")
def admin_recetas():
    if not administrador_conectado():
        return redirect("/iniciar-sesion.html")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categoria ORDER BY nombre")
    categorias = cursor.fetchall()
    cursor.execute("""
        SELECT receta.*, categoria.nombre AS categoria,
               usuario.usuario AS autor_usuario
        FROM receta
        INNER JOIN categoria ON receta.id_categoria = categoria.id
        INNER JOIN usuario ON receta.id_usuario = usuario.id
        ORDER BY receta.fechahora DESC
    """)
    recetas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template(
        "admin-recetas.html",
        recetas=recetas,
        categorias=categorias
    )


@app.route("/admin/receta/<int:id_receta>/estado", methods=["POST"])
def admin_cambiar_estado_receta(id_receta):
    if not administrador_conectado():
        return redirect("/iniciar-sesion.html")

    estado = request.form["estado"]

    if estado in ["en_revision", "disponible", "no_disponible"]:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE receta SET estado = %s WHERE id = %s",
            (estado, id_receta)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    return redirect("/admin-recetas.html")


@app.route("/admin-categorias.html", methods=["GET", "POST"])
def admin_categorias():
    if not administrador_conectado():
        return redirect("/iniciar-sesion.html")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["nombre"].strip()

        if nombre != "":
            try:
                cursor.execute(
                    "INSERT INTO categoria (nombre) VALUES (%s)",
                    (nombre,)
                )
                conexion.commit()
            except mysql.connector.IntegrityError:
                flash("Esa categoría ya existe.")

    cursor.execute("SELECT * FROM categoria ORDER BY nombre")
    categorias = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template("admin-categorias.html", categorias=categorias)


@app.route("/admin/categoria/<int:id_categoria>/eliminar", methods=["POST"])
def admin_eliminar_categoria(id_categoria):
    if not administrador_conectado():
        return redirect("/iniciar-sesion.html")

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("DELETE FROM categoria WHERE id = %s", (id_categoria,))
        conexion.commit()
    except mysql.connector.IntegrityError:
        flash("No se puede eliminar una categoría que tiene recetas.")

    cursor.close()
    conexion.close()
    return redirect("/admin-categorias.html")


@app.route("/admin-usuarios.html")
def admin_usuarios():
    if not administrador_conectado():
        return redirect("/iniciar-sesion.html")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT usuario.id, usuario.nombre, usuario.apellido,
               usuario.mail, usuario.usuario, usuario.estado,
               usuario.rol, COUNT(receta.id) AS cantidad_recetas
        FROM usuario
        LEFT JOIN receta ON usuario.id = receta.id_usuario
        GROUP BY usuario.id, usuario.nombre, usuario.apellido,
                 usuario.mail, usuario.usuario, usuario.estado, usuario.rol
        ORDER BY usuario.nombre, usuario.apellido
    """)
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template("admin-usuarios.html", usuarios=usuarios)


@app.route("/admin/usuario/<int:id_usuario>/estado", methods=["POST"])
def admin_cambiar_estado_usuario(id_usuario):
    if not administrador_conectado():
        return redirect("/iniciar-sesion.html")

    estado = request.form["estado"]

    if estado in ["activo", "inactivo"]:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE usuario SET estado = %s WHERE id = %s",
            (estado, id_usuario)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    return redirect("/admin-usuarios.html")


if __name__ == "__main__":
    app.run(debug=True)
