CREATE DATABASE IF NOT EXISTS recetapp
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE recetapp;

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    apellido VARCHAR(30) NOT NULL,
    mail VARCHAR(50) NOT NULL UNIQUE,
    usuario VARCHAR(30) NOT NULL UNIQUE,
    contrasenia VARCHAR(255) NOT NULL,
    sobre_mi VARCHAR(300),
    estado ENUM('activo', 'inactivo') NOT NULL DEFAULT 'activo',
    rol ENUM('usuario', 'admin') NOT NULL DEFAULT 'usuario'
) ENGINE = InnoDB;

CREATE TABLE categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE
) ENGINE = InnoDB;

CREATE TABLE receta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_categoria INT NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    descripcion TEXT NOT NULL,
    ingredientes TEXT NOT NULL,
    preparacion TEXT NOT NULL,
    tiempo INT NOT NULL,
    porciones INT NOT NULL,
    dificultad ENUM('facil', 'media', 'dificil') NOT NULL,
    estado ENUM('en_revision', 'disponible', 'no_disponible')
        NOT NULL DEFAULT 'en_revision',
    fechahora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    imagen VARCHAR(100),

    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
        ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id)
        ON DELETE RESTRICT
) ENGINE = InnoDB;

CREATE TABLE favorito (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_receta INT NOT NULL,
    fechahora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (id_usuario, id_receta),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
        ON DELETE CASCADE,
    FOREIGN KEY (id_receta) REFERENCES receta(id)
        ON DELETE CASCADE
) ENGINE = InnoDB;

CREATE TABLE comentario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_receta INT NOT NULL,
    contenido TEXT NOT NULL,
    fechahora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
        ON DELETE CASCADE,
    FOREIGN KEY (id_receta) REFERENCES receta(id)
        ON DELETE CASCADE
) ENGINE = InnoDB;

INSERT INTO categoria (nombre) VALUES
    ('Pastas'),
    ('Ensaladas'),
    ('Postres'),
    ('Comidas rápidas'),
    ('Otras');
