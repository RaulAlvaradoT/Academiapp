-- Script SQL para inicializar base de datos AcademiApp en MySQL
-- Copiar y pegar en phpMyAdmin

-- Tabla de Diplomados
CREATE TABLE IF NOT EXISTS diplomados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    clave VARCHAR(50) UNIQUE NOT NULL,
    modalidad VARCHAR(50) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    num_mensualidades INT NOT NULL,
    alumnos_inscritos INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'Activo'
);

-- Tabla de Alumnos
CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(50) NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    diplomado_id INT,
    diplomado_clave VARCHAR(50) NOT NULL,
    telefono VARCHAR(50) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    fecha_inscripcion DATE NOT NULL,
    pago_inscripcion DECIMAL(10,2) NOT NULL,
    mensualidad DECIMAL(10,2) NOT NULL,
    num_mensualidades INT NOT NULL,
    total_diplomado DECIMAL(10,2) NOT NULL,
    curp VARCHAR(50) NOT NULL,
    fecha_baja DATE,
    motivo_baja TEXT,
    FOREIGN KEY (diplomado_id) REFERENCES diplomados(id)
);

-- Tabla de Pagos
CREATE TABLE IF NOT EXISTS pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    num_mensualidad INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha_pago DATE NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
);

-- Tabla de Gastos
CREATE TABLE IF NOT EXISTS gastos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    concepto VARCHAR(255) NOT NULL,
    monto DECIMAL(10,2) NOT NULL
);

-- Tabla de Calendario
CREATE TABLE IF NOT EXISTS calendario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    diplomado_clave VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    modulo INT NOT NULL,
    FOREIGN KEY (diplomado_clave) REFERENCES diplomados(clave)
);
