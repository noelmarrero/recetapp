RECETAPP - ENTREGA CON BASE DE DATOS

ALCANCE DE ESTA ENTREGA

La conexión con la base de datos se usa solamente para:

- Registrar usuarios.
- Iniciar y cerrar sesión.
- Cargar recetas.
- Mostrar las recetas cargadas en la página principal.

Las demás pantallas se conservan como parte del diseño realizado en las
entregas anteriores, pero todavía no tienen conexión con la base de datos.

ESTRUCTURA DEL PROYECTO

- Los archivos HTML están en la carpeta principal.
- Los estilos están en css.
- Los archivos JavaScript están en js.
- Las imágenes están en imagenes.
- El servidor de Python está en py/app.py.
- No se usan carpetas templates ni static.

1. Abrir XAMPP e iniciar MySQL.

2. Entrar a http://localhost/phpmyadmin.

3. Importar el archivo base_datos.sql.

   Si ya se había importado la versión anterior de la base y todavía no hay
   información importante, eliminar la base recetapp desde phpMyAdmin y volver
   a importar este archivo. Esta versión usa VARCHAR(255) para guardar el hash
   de la contraseña.

4. Abrir esta carpeta en VS Code.

5. Instalar las dependencias desde la terminal:

   pip install -r requirements.txt

6. Ejecutar la aplicación:

   python py/app.py

7. Abrir en el navegador:

   http://127.0.0.1:5000

DATOS DE CONEXIÓN

La conexión está al principio de app.py:

    host="localhost"
    user="root"
    password=""
    database="recetapp"

Si el usuario root de MySQL tiene contraseña, escribirla en password.

CREAR UN ADMINISTRADOR

1. Registrar un usuario normalmente desde la página.
2. Entrar a phpMyAdmin, abrir recetapp y seleccionar la pestaña SQL.
3. Ejecutar, reemplazando el correo por el que se registró:

   UPDATE usuario SET rol = 'admin' WHERE mail = 'correo@ejemplo.com';

4. Cerrar sesión y volver a iniciar. Se abrirá el panel de administrador.

IMÁGENES

El proyecto conserva la carpeta imagenes. Se pueden copiar allí los
archivos pasta.jpg, ensalada.jpg y torta.jpg. Las nuevas imágenes subidas desde
el formulario también se guardan en esa carpeta.
