CREATE DATABASE RegistroAcademicoColegio;
GO
USE RegistroAcademicoColegio;

CREATE TABLE Estudiantes (
    EstudianteID INT PRIMARY KEY IDENTITY,
    Nombre NVARCHAR(50),
    Apellido NVARCHAR(50),
    FechaNacimiento DATE,
    Direccion NVARCHAR(100),
    Telefono NVARCHAR(15),
    Email NVARCHAR(50)
);

CREATE TABLE Profesores (
    ProfesorID INT PRIMARY KEY IDENTITY,
    Nombre NVARCHAR(50),
    Apellido NVARCHAR(50),
    Especialidad NVARCHAR(50),
    Telefono NVARCHAR(15),
    Email NVARCHAR(50)
);

CREATE TABLE Cursos (
    CursoID INT PRIMARY KEY IDENTITY,
    Nombre NVARCHAR(50),
    Descripcion NVARCHAR(100),
    Creditos INT
);

-- Tabla intermedia para asociar profesores con cursos
CREATE TABLE ProfesoresCursos (
    ProfesorID INT FOREIGN KEY REFERENCES Profesores(ProfesorID),
    CursoID INT FOREIGN KEY REFERENCES Cursos(CursoID),
    PRIMARY KEY (ProfesorID, CursoID)
);

CREATE TABLE Inscripciones (
    InscripcionID INT PRIMARY KEY IDENTITY,
    EstudianteID INT FOREIGN KEY REFERENCES Estudiantes(EstudianteID),
    CursoID INT FOREIGN KEY REFERENCES Cursos(CursoID),
    FechaInscripcion DATE
);



CREATE TABLE Calificaciones (
    CalificacionID INT PRIMARY KEY IDENTITY,
    EstudianteID INT FOREIGN KEY REFERENCES Estudiantes(EstudianteID),
    CursoID INT FOREIGN KEY REFERENCES Cursos(CursoID),
    Nota DECIMAL(4, 2) CHECK (Nota BETWEEN 0 AND 10)
);




CREATE TABLE Asistencias (
    AsistenciaID INT PRIMARY KEY IDENTITY,
    EstudianteID INT FOREIGN KEY REFERENCES Estudiantes(EstudianteID),
    CursoID INT FOREIGN KEY REFERENCES Cursos(CursoID),
    Fecha DATE,
    Estado NVARCHAR(10) CHECK (Estado IN ('Presente', 'Ausente', 'Tarde'))
);

--procedimiento alacenado para optener los estudiantes
CREATE PROCEDURE ObtenerEstudiantes
AS
BEGIN
    SELECT EstudianteID, Nombre, Apellido, FechaNacimiento, Direccion, Telefono, Email
    FROM Estudiantes;
END;



--procedimiento almacnado para la tabal profesores 


CREATE PROCEDURE ObtenerProfesores
AS
BEGIN
    SELECT ProfesorID, Nombre, Apellido, Especialidad, Telefono, Email
    FROM Profesores;
END;



--procedimiento almacenado para optener cursos

CREATE PROCEDURE ObtenerCursos
AS
BEGIN
    -- Selecciona todos los cursos de la tabla Cursos
    SELECT CursoID, Nombre, Descripcion, Creditos
    FROM Cursos;
END;


--tabla usuario

CREATE TABLE Usuarios (
    UsuarioID INT PRIMARY KEY IDENTITY(1,1),  
    Nombre NVARCHAR(50) NOT NULL,             
    Apellido NVARCHAR(50) NOT NULL,           
    Email NVARCHAR(100) UNIQUE NOT NULL,      
    Username NVARCHAR(50) UNIQUE NOT NULL,    
    PasswordHash NVARCHAR(255) NOT NULL,     
    Rol NVARCHAR(20) CHECK (Rol IN ('admin', 'profesor', 'estudiante')) NOT NULL, 
    Estado NVARCHAR(10) CHECK (Estado IN ('activo', 'inactivo')) DEFAULT 'activo',
    FechaCreacion DATETIME DEFAULT GETDATE(),
    UltimoLogin DATETIME NULL                 
);




-- Procedimiento para agregar un usuario
CREATE PROCEDURE spAgregarUsuario
    @Nombre NVARCHAR(50),
    @Apellido NVARCHAR(50),
    @Email NVARCHAR(100),
    @Username NVARCHAR(50),
    @PasswordHash NVARCHAR(255),
    @Rol NVARCHAR(20)
AS
BEGIN
    INSERT INTO Usuarios (Nombre, Apellido, Email, Username, PasswordHash, Rol)
    VALUES (@Nombre, @Apellido, @Email, @Username, @PasswordHash, @Rol)
END
GO

-- Procedimiento para actualizar un usuario
CREATE PROCEDURE spActualizarUsuario
    @UsuarioID INT,
    @Nombre NVARCHAR(50),
    @Apellido NVARCHAR(50),
    @Email NVARCHAR(100),
    @Username NVARCHAR(50),
    @Rol NVARCHAR(20),
    @Estado NVARCHAR(10)
AS
BEGIN
    UPDATE Usuarios
    SET Nombre = @Nombre, Apellido = @Apellido, Email = @Email, Username = @Username, Rol = @Rol, Estado = @Estado
    WHERE UsuarioID = @UsuarioID
END
GO

-- Procedimiento para eliminar un usuario
CREATE PROCEDURE spEliminarUsuario
    @UsuarioID INT
AS
BEGIN
    DELETE FROM Usuarios
    WHERE UsuarioID = @UsuarioID
END
GO

-- Procedimiento para obtener todos los usuarios
CREATE PROCEDURE spObtenerUsuarios
AS
BEGIN
    SELECT UsuarioID, Nombre, Apellido, Email, Username, Rol, Estado, FechaCreacion, UltimoLogin
    FROM Usuarios
END
GO

-- Procedimiento para obtener un usuario por ID
CREATE PROCEDURE spObtenerUsuarioPorID
    @UsuarioID INT
AS
BEGIN
    SELECT UsuarioID, Nombre, Apellido, Email, Username, Rol, Estado, FechaCreacion, UltimoLogin
    FROM Usuarios
    WHERE UsuarioID = @UsuarioID
END
GO


SELECT * FROM Usuarios

