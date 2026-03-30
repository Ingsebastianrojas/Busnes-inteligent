-- =========================
-- LIMPIAR TODO (opcional)
-- =========================
DROP TABLE IF EXISTS asistencias, notas, estudiante_materia, estudiante_semestre, estudiantes, materias, semestres CASCADE;

-- =========================
-- CREAR TABLAS
-- =========================

CREATE TABLE estudiantes (
    id_estudiante SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE,
    fecha_nacimiento DATE
);

CREATE TABLE semestres (
    id_semestre SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE
);

CREATE TABLE materias (
    id_materia SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    creditos INT
);

CREATE TABLE estudiante_materia (
    id_estudiante_materia SERIAL PRIMARY KEY,
    id_estudiante INT REFERENCES estudiantes(id_estudiante),
    id_materia INT REFERENCES materias(id_materia),
    id_semestre INT REFERENCES semestres(id_semestre)
);

CREATE TABLE notas (
    id_nota SERIAL PRIMARY KEY,
    id_estudiante_materia INT REFERENCES estudiante_materia(id_estudiante_materia),
    nota DECIMAL(5,2),
    tipo VARCHAR(50)
);

CREATE TABLE asistencias (
    id_asistencia SERIAL PRIMARY KEY,
    id_estudiante_materia INT REFERENCES estudiante_materia(id_estudiante_materia),
    fecha DATE,
    asistio BOOLEAN
);

-- =========================
-- INSERTAR DATOS
-- =========================

-- Estudiantes
INSERT INTO estudiantes (nombre, apellido, correo, fecha_nacimiento) VALUES
('Juan','Perez','juan1@mail.com','2000-01-10'),
('Maria','Gomez','maria2@mail.com','2001-02-12'),
('Carlos','Lopez','carlos3@mail.com','1999-03-15'),
('Ana','Martinez','ana4@mail.com','2000-04-20'),
('Luis','Rodriguez','luis5@mail.com','2001-05-25'),
('Sofia','Hernandez','sofia6@mail.com','2002-06-18'),
('Pedro','Diaz','pedro7@mail.com','1998-07-22'),
('Laura','Torres','laura8@mail.com','2000-08-30'),
('Diego','Ramirez','diego9@mail.com','2001-09-14'),
('Valentina','Cruz','valentina10@mail.com','2002-10-05'),
('Andres','Vargas','andres11@mail.com','1999-11-11'),
('Camila','Castro','camila12@mail.com','2000-12-09'),
('Jorge','Rios','jorge13@mail.com','1998-01-17'),
('Daniela','Morales','daniela14@mail.com','2001-02-28'),
('Felipe','Ortiz','felipe15@mail.com','2002-03-03'),
('Paula','Silva','paula16@mail.com','2000-04-07'),
('Santiago','Mendez','santiago17@mail.com','1999-05-19'),
('Natalia','Reyes','natalia18@mail.com','2001-06-23'),
('Ricardo','Navarro','ricardo19@mail.com','2002-07-29'),
('Juliana','Pardo','juliana20@mail.com','2000-08-11');

-- Semestre
INSERT INTO semestres (nombre, fecha_inicio, fecha_fin) VALUES
('2024-1','2024-01-15','2024-06-15');

-- Materias
INSERT INTO materias (nombre, creditos) VALUES
('Matematicas',3),
('Programacion',4),
('Bases de Datos',3),
('IA',3),
('Estadistica',2),
('Fisica',3);

-- Relación estudiante - materia (CLAVE)
INSERT INTO estudiante_materia (id_estudiante, id_materia, id_semestre) VALUES
(1,1,1),(2,2,1),(3,3,1),(4,1,1),(5,2,1),
(6,3,1),(7,1,1),(8,2,1),(9,3,1),(10,1,1),
(11,2,1),(12,3,1),(13,1,1),(14,2,1),(15,3,1),
(16,1,1),(17,2,1),(18,3,1),(19,1,1),(20,2,1);

-- Notas
INSERT INTO notas (id_estudiante_materia, nota, tipo) VALUES
(1,3.5,'parcial'),(2,4.2,'final'),(3,2.8,'quiz'),(4,3.9,'parcial'),
(5,4.5,'final'),(6,3.0,'quiz'),(7,2.5,'parcial'),(8,4.8,'final'),
(9,3.3,'quiz'),(10,3.7,'parcial'),(11,4.1,'final'),(12,2.9,'quiz'),
(13,3.6,'parcial'),(14,4.4,'final'),(15,3.2,'quiz'),(16,2.7,'parcial'),
(17,4.0,'final'),(18,3.8,'quiz'),(19,4.6,'parcial'),(20,3.1,'final');

-- Asistencias
INSERT INTO asistencias (id_estudiante_materia, fecha, asistio) VALUES
(1,'2025-03-01',true),(2,'2025-03-01',false),(3,'2025-03-01',true),
(4,'2025-03-01',true),(5,'2025-03-01',false),(6,'2025-03-01',true),
(7,'2025-03-01',false),(8,'2025-03-01',true),(9,'2025-03-01',true),
(10,'2025-03-01',false),(11,'2025-03-01',true),(12,'2025-03-01',true),
(13,'2025-03-01',false),(14,'2025-03-01',true),(15,'2025-03-01',true),
(16,'2025-03-01',false),(17,'2025-03-01',true),(18,'2025-03-01',false),
(19,'2025-03-01',true),(20,'2025-03-01',true);





select * from estudiantes,asistencias,notas,materias  ;