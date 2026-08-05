-- =====================================================================
-- Base de datos: administrador_procesos
-- Sistema de control de inventario de GPS e instalaciones
-- Generado según especificación de tipos/longitudes (Excel de formato)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS administrador_procesos
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE administrador_procesos;

-- ---------------------------------------------------------------------
-- Tabla: Usuarios
-- ---------------------------------------------------------------------
CREATE TABLE Usuarios (
    ID_usuario   INT AUTO_INCREMENT PRIMARY KEY,
    Nombre       VARCHAR(100) NOT NULL,
    Correo       VARCHAR(150) NOT NULL UNIQUE,
    Contrasena   VARCHAR(255) NOT NULL,
    Rol          VARCHAR(30)  NOT NULL,
    CONSTRAINT chk_usuarios_rol CHECK (Rol IN ('Administrador', 'Operaciones'))
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabla: Clientes
-- ---------------------------------------------------------------------
CREATE TABLE Clientes (
    ID_Cliente   INT AUTO_INCREMENT PRIMARY KEY,
    Nombre       VARCHAR(150) NOT NULL,
    RncCedula    VARCHAR(20)  NOT NULL UNIQUE,
    Telefono     VARCHAR(20)  NOT NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabla: Tecnico
-- ---------------------------------------------------------------------
CREATE TABLE Tecnico (
    ID_tecnico   INT AUTO_INCREMENT PRIMARY KEY,
    Nombre       VARCHAR(100) NOT NULL,
    Telefono     VARCHAR(20)  NOT NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabla: Inventario
-- ---------------------------------------------------------------------
CREATE TABLE Inventario (
    ID_GPS             INT AUTO_INCREMENT PRIMARY KEY,
    IMEI_CodigoBarras  VARCHAR(50) NOT NULL UNIQUE,
    Modelo             VARCHAR(50) NOT NULL,
    Estado             VARCHAR(20) NOT NULL DEFAULT 'Disponible',
    ID_tecnico         INT NULL,
    FechaEntrega       DATE NULL,
    CONSTRAINT chk_inventario_estado CHECK (Estado IN ('Disponible', 'Asignado', 'Instalado')),
    CONSTRAINT fk_inventario_tecnico FOREIGN KEY (ID_tecnico)
        REFERENCES Tecnico(ID_tecnico)
        ON UPDATE CASCADE
        ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabla: Controles  (llamada "PROCESO" en el documento de formato)
-- ---------------------------------------------------------------------
CREATE TABLE Controles (
    ID_Control        INT AUTO_INCREMENT PRIMARY KEY,
    FechaInstalacion  DATE NOT NULL DEFAULT (CURRENT_DATE),
    ID_cliente        INT NOT NULL,
    ID_tecnico        INT NOT NULL,
    ID_GPS            INT NOT NULL,
    ID_Usuario        INT NOT NULL,
    Tipo              VARCHAR(20) NOT NULL,
    Chasis            VARCHAR(50) NOT NULL,
    Modelo            VARCHAR(50) NOT NULL,
    Ano               INT NOT NULL,
    Color             VARCHAR(30) NOT NULL,
    Placa             VARCHAR(20) NULL,

    CONSTRAINT chk_controles_tipo CHECK (Tipo IN ('Instalacion', 'Desinstalacion', 'Reinstalacion', 'Cambio')),

    INDEX idx_controles_chasis (Chasis),

    CONSTRAINT fk_controles_cliente FOREIGN KEY (ID_cliente)
        REFERENCES Clientes(ID_Cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_controles_tecnico FOREIGN KEY (ID_tecnico)
        REFERENCES Tecnico(ID_tecnico)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_controles_gps FOREIGN KEY (ID_GPS)
        REFERENCES Inventario(ID_GPS)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_controles_usuario FOREIGN KEY (ID_Usuario)
        REFERENCES Usuarios(ID_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =====================================================================
-- Verificación
-- =====================================================================
SHOW TABLES;
