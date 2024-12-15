from app.config import get_db_connection
import hashlib

def serialize_estudiante(row):
    return {
        "EstudianteID": row.EstudianteID,
        "Nombre": row.Nombre,
        "Apellido": row.Apellido,
        "FechaNacimiento": row.FechaNacimiento.isoformat() if hasattr(row.FechaNacimiento, 'isoformat') else row.FechaNacimiento,
        "Direccion": row.Direccion,
        "Telefono": row.Telefono,
        "Email": row.Email
    }


def obtener_estudiantes():
    connection = get_db_connection()
    estudiantes = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("EXEC ObtenerEstudiantes")
            records = cursor.fetchall()
            estudiantes = [serialize_estudiante(row) for row in records]
        except Exception as e:
            print("Error al obtener estudiantes:", e)
        finally:
            cursor.close()
            connection.close()
    return estudiantes

def agregar_estudiante(nombre, apellido, fecha_nacimiento, direccion, telefono, email):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Estudiantes (Nombre, Apellido, FechaNacimiento, Direccion, Telefono, Email) VALUES (?, ?, ?, ?, ?, ?)", 
                (nombre, apellido, fecha_nacimiento, direccion, telefono, email)
            )
            connection.commit()
        except Exception as e:
            print("Error al agregar estudiante:", e)
        finally:
            cursor.close()
            connection.close()

def actualizar_estudiante(estudiante_id, nombre, apellido, fecha_nacimiento, direccion, telefono, email):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE Estudiantes SET Nombre = ?, Apellido = ?, FechaNacimiento = ?, Direccion = ?, Telefono = ?, Email = ? WHERE EstudianteID = ?",
                (nombre, apellido, fecha_nacimiento, direccion, telefono, email, estudiante_id)
            )
            connection.commit()
        except Exception as e:
            print("Error al actualizar estudiante:", e)
        finally:
            cursor.close()
            connection.close()

def eliminar_estudiante(estudiante_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Estudiantes WHERE EstudianteID = ?", (estudiante_id,))
            connection.commit()
        except Exception as e:
            print("Error al eliminar estudiante:", e)
        finally:
            cursor.close()
            connection.close()

def obtener_estudiante_por_id(estudiante_id):
    connection = get_db_connection()
    estudiante = None
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Estudiantes WHERE EstudianteID = ?", (estudiante_id,))
            row = cursor.fetchone()
            if row:
                estudiante = serialize_estudiante(row)
        except Exception as e:
            print("Error al obtener estudiante por ID:", e)
        finally:
            cursor.close()
            connection.close()
    return estudiante




#models profesores


def serialize_profesor(row):
    return {
        "ProfesorID": row.ProfesorID,
        "Nombre": row.Nombre,
        "Apellido": row.Apellido,
        "Especialidad": row.Especialidad,
        "Telefono": row.Telefono,
        "Email": row.Email,
        "Cursos": row.Cursos.split(", ") if row.Cursos else []  # Dividir en lista si no es None
    }

# Funcionalidades CRUD

from app.config import get_db_connection

def obtener_profesores():
    connection = get_db_connection()
    profesores = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("EXEC ObtenerProfesores")  
            records = cursor.fetchall()
            profesores = [serialize_profesor(row) for row in records]
        except Exception as e:
            print("Error al obtener profesores:", e)
        finally:
            cursor.close()
            connection.close()
    return profesores


def agregar_profesor(nombre, apellido, especialidad, telefono, email):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Profesores (Nombre, Apellido, Especialidad, Telefono, Email) VALUES (?, ?, ?, ?, ?)",
                (nombre, apellido, especialidad, telefono, email)
            )
            connection.commit()
        except Exception as e:
            print("Error al agregar profesor:", e)
        finally:
            cursor.close()
            connection.close()

def actualizar_profesor(profesor_id, nombre, apellido, especialidad, telefono, email):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE Profesores SET Nombre = ?, Apellido = ?, Especialidad = ?, Telefono = ?, Email = ? WHERE ProfesorID = ?",
                (nombre, apellido, especialidad, telefono, email, profesor_id)
            )
            connection.commit()
        except Exception as e:
            print("Error al actualizar profesor:", e)
        finally:
            cursor.close()
            connection.close()

def eliminar_profesor(profesor_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Profesores WHERE ProfesorID = ?", (profesor_id,))
            connection.commit()
        except Exception as e:
            print("Error al eliminar profesor:", e)
        finally:
            cursor.close()
            connection.close()

def obtener_profesor_por_id(profesor_id):
    connection = get_db_connection()
    profesor = None
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    p.ProfesorID, 
                    p.Nombre, 
                    p.Apellido, 
                    p.Especialidad, 
                    p.Telefono, 
                    p.Email,
                    STUFF((
                        SELECT ', ' + c.Nombre
                        FROM ProfesoresCursos pc
                        INNER JOIN Cursos c ON pc.CursoID = c.CursoID
                        WHERE pc.ProfesorID = p.ProfesorID
                        FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '') AS Cursos
                FROM Profesores p
                WHERE p.ProfesorID = ?
            """, (profesor_id,))
            row = cursor.fetchone()
            if row:
                profesor = serialize_profesor(row)
            else:
                print("Profesor no encontrado.")
        except Exception as e:
            print("Error al obtener profesor por ID:", e)
        finally:
            cursor.close()
            connection.close()
    return profesor






#models para curso

def serialize_curso(row):
    return {
        "CursoID": row.CursoID,
        "Nombre": row.Nombre,
        "Descripcion": row.Descripcion,
        "Creditos": row.Creditos
    }

# funciones crud para cursos

def obtener_cursos():
    connection = get_db_connection()
    cursos = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("EXEC ObtenerCursos")  
            records = cursor.fetchall()
            cursos = [serialize_curso(row) for row in records]
        except Exception as e:
            print("Error al obtener cursos:", e)
        finally:
            cursor.close()
            connection.close()
    return cursos

def agregar_curso(nombre, descripcion, creditos):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Cursos (Nombre, Descripcion, Creditos) VALUES (?, ?, ?)",
                (nombre, descripcion, creditos)
            )
            connection.commit()
        except Exception as e:
            print("Error al agregar curso:", e)
        finally:
            cursor.close()
            connection.close()

def actualizar_curso(curso_id, nombre, descripcion, creditos):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE Cursos SET Nombre = ?, Descripcion = ?, Creditos = ? WHERE CursoID = ?",
                (nombre, descripcion, creditos, curso_id)
            )
            connection.commit()
        except Exception as e:
            print("Error al actualizar curso:", e)
        finally:
            cursor.close()
            connection.close()

def eliminar_curso_db(curso_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Cursos WHERE CursoID = ?", (curso_id,))
            connection.commit()
        except Exception as e:
            print("Error al eliminar curso:", e)
        finally:
            cursor.close()
            connection.close()

def obtener_curso_por_id(curso_id):
    connection = get_db_connection()
    curso = None
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Cursos WHERE CursoID = ?", (curso_id,))
            row = cursor.fetchone()
            if row:
                curso = serialize_curso(row)
        except Exception as e:
            print("Error al obtener curso por ID:", e)
        finally:
            cursor.close()
            connection.close()
    return curso



#models para inscripcion  MODIFICADO
def serialize_inscripcion(row):
    return {
        "InscripcionID": row.InscripcionID,
        "EstudianteNombre": row.EstudianteNombre,
        "CursoNombre": row.CursoNombre,
        "FechaInscripcion": row.FechaInscripcion.isoformat() if hasattr(row.FechaInscripcion, 'isoformat') else row.FechaInscripcion,
        "CursoID": row.CursoID,
        "EstudianteID": row.EstudianteID
    }

#funcines crud para inscripcion   MODIFICADO
def obtener_inscripciones():
    connection = get_db_connection()
    inscripciones = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    i.InscripcionID,
                    e.EstudianteID,
                    concat(e.Nombre, ' ', e.Apellido) AS NombreEstudiante,
                    c.CursoID,
                    c.Nombre AS NombreCurso,
                    i.FechaInscripcion
                FROM 
                    Inscripciones i
                JOIN 
                    Estudiantes e ON i.EstudianteID = e.EstudianteID
                JOIN 
                    Cursos c ON i.CursoID = c.CursoID
            """)
            records = cursor.fetchall()
            inscripciones = [
                {
                    "InscripcionID": row.InscripcionID,
                    "EstudianteID": row.EstudianteID,
                    "NombreEstudiante": row.NombreEstudiante,
                    "CursoID": row.CursoID,
                    "NombreCurso": row.NombreCurso,
                    "FechaInscripcion": row.FechaInscripcion.isoformat() if hasattr(row.FechaInscripcion, 'isoformat') else row.FechaInscripcion
                }
                for row in records
            ]
        except Exception as e:
            print("Error al obtener inscripciones:", e)
        finally:
            cursor.close()
            connection.close()
    return inscripciones



def agregar_inscripcion(estudiante_id, curso_id, fecha_inscripcion):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Inscripciones (EstudianteID, CursoID, FechaInscripcion) VALUES (?, ?, ?)",
                (estudiante_id, curso_id, fecha_inscripcion)
            )
            connection.commit()
        except Exception as e:
            print("Error al agregar inscripción:", e)
        finally:
            cursor.close()
            connection.close()

def actualizar_inscripcion(inscripcion_id, estudiante_id, curso_id, fecha_inscripcion):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE Inscripciones SET EstudianteID = ?, CursoID = ?, FechaInscripcion = ? WHERE InscripcionID = ?",
                (estudiante_id, curso_id, fecha_inscripcion, inscripcion_id)
            )
            connection.commit()
        except Exception as e:
            print("Error al actualizar inscripción:", e)
        finally:
            cursor.close()
            connection.close()

def eliminar_inscripcion(inscripcion_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Inscripciones WHERE InscripcionID = ?", (inscripcion_id,))
            connection.commit()
        except Exception as e:
            print("Error al eliminar inscripción:", e)
        finally:
            cursor.close()
            connection.close()


# metodo MODIFICADO
def obtener_inscripcion_por_id(inscripcion_id):
    connection = get_db_connection()
    inscripcion = None
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    i.InscripcionID,
                    e.EstudianteID,
                    e.Nombre AS EstudianteNombre,
                    c.CursoID,
                    c.Nombre AS CursoNombre,
                    i.FechaInscripcion
                FROM 
                    Inscripciones i
                JOIN 
                    Estudiantes e ON i.EstudianteID = e.EstudianteID
                JOIN 
                    Cursos c ON i.CursoID = c.CursoID
                WHERE 
                    i.InscripcionID = ?
            """, (inscripcion_id,))
            row = cursor.fetchone()
            if row:
                inscripcion = serialize_inscripcion(row)
        except Exception as e:
            print("Error al obtener inscripción por ID:", e)
        finally:
            cursor.close()
            connection.close()
    return inscripcion

# Obtiene los cursos inscritos por un estudiante
def obtener_cursos_por_estudiante_id(estudiante_id):
    connection = get_db_connection()
    cursos = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT c.CursoID, c.Nombre
                FROM Inscripciones i
                JOIN Cursos c ON i.CursoID = c.CursoID
                WHERE i.EstudianteID = ?
            """, (estudiante_id,))
            cursos = [{"CursoID": row[0], "Nombre": row[1]} for row in cursor.fetchall()]
        except Exception as e:
            print("Error al obtener cursos inscritos:", e)
        finally:
            cursor.close()
            connection.close()
    return cursos


#models para calificaion

def serialize_calificacion(row):
    return {
        "CalificacionID": row[0],   
        "EstudianteID": row[1],     
        "CursoID": row[2],          
        "Nota": row[3]              
    }



#funciones crud para calificaion


def serialize_calificacion(row):
    """Serializa la fila de la base de datos a un diccionario."""
    return {
        "CalificacionID": row[0],           # Calificación ID
        "EstudianteID": row[1],             # Estudiante ID
        "CursoID": row[2],                  # Curso ID
        "Nota": row[3],                     # Nota
        "NombreEstudiante": row[4],         # Nombre completo del estudiante
        "NombreCurso": row[5]               # Nombre del curso
    }


def obtener_calificaciones():
    """Obtiene las calificaciones, nombres de estudiantes y cursos desde la base de datos."""
  
    connection = get_db_connection()
    calificaciones = []
    

    if connection:
        try:
            cursor = connection.cursor()
            
           
            cursor.execute("""
                SELECT c.CalificacionID, e.EstudianteID, cu.CursoID, c.Nota, concat(e.Nombre, ' ', e.Apellido) AS NombreEstudiante, cu.Nombre AS NombreCurso
                FROM Calificaciones c
                JOIN Estudiantes e ON c.EstudianteID = e.EstudianteID
                JOIN Cursos cu ON c.CursoID = cu.CursoID
            """)
            
           
            for row in cursor:
                calificaciones.append(serialize_calificacion(row))
        
        except Exception as e:
           
            print("Error al obtener calificaciones:", e)
            return {"error": "No se pudo obtener calificaciones."}
        
        finally:
           
            cursor.close()
            connection.close()

    return calificaciones


def agregar_calificacion(estudiante_id, curso_id, nota):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Calificaciones (EstudianteID, CursoID, Nota) VALUES (?, ?, ?)",
                (estudiante_id, curso_id, nota)
            )
            connection.commit()
        except Exception as e:
            print("Error al agregar calificación:", e)
        finally:
            cursor.close()
            connection.close()

def actualizar_calificacion(calificacion_id, estudiante_id, curso_id, nota):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE Calificaciones SET EstudianteID = ?, CursoID = ?, Nota = ? WHERE CalificacionID = ?",
                (estudiante_id, curso_id, nota, calificacion_id)
            )
            connection.commit()
        except Exception as e:
            print("Error al actualizar calificación:", e)
        finally:
            cursor.close()
            connection.close()

def eliminar_calificacion(calificacion_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Calificaciones WHERE CalificacionID = ?", (calificacion_id,))
            connection.commit()
        except Exception as e:
            print("Error al eliminar calificación:", e)
        finally:
            cursor.close()
            connection.close()

# MODIFICADO
def obtener_calificacion_por_id(calificacion_id):
    connection = get_db_connection()
    calificacion = None
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT c.CalificacionID, e.EstudianteID, cu.CursoID, c.Nota, concat(e.Nombre, ' ', e.Apellido) AS NombreEstudiante, cu.Nombre AS NombreCurso FROM Calificaciones c JOIN Estudiantes e ON c.EstudianteID = e.EstudianteID JOIN Cursos cu ON c.CursoID = cu.CursoID WHERE c.CalificacionID = ?", (calificacion_id,))
            row = cursor.fetchone()
            if row:
                calificacion = serialize_calificacion(row)
        except Exception as e:
            print("Error al obtener calificación por ID:", e)
        finally:
            cursor.close()
            connection.close()
    return calificacion



#MODELS ASITENCIAS

def obtener_asistencias():
    connection = get_db_connection()
    asistencias = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    a.AsistenciaID,
                    e.EstudianteID,
                    concat(e.Nombre, ' ', e.Apellido) AS NombreEstudiante,
                    c.CursoID,
                    c.Nombre AS NombreCurso,
                    a.Fecha,
                    a.Estado
                FROM 
                    Asistencias a
                JOIN 
                    Estudiantes e ON a.EstudianteID = e.EstudianteID
                JOIN 
                    Cursos c ON a.CursoID = c.CursoID
            """)
            records = cursor.fetchall()
            asistencias = [
                {
                    "AsistenciaID": row.AsistenciaID,
                    "EstudianteID": row.EstudianteID,
                    "NombreEstudiante": row.NombreEstudiante,
                    "CursoID": row.CursoID,
                    "NombreCurso": row.NombreCurso,
                    "Fecha": row.Fecha.isoformat() if hasattr(row.Fecha, 'isoformat') else row.Fecha,
                    "Estado": row.Estado
                }
                for row in records
            ]
        except Exception as e:
            print("Error al obtener asistencias:", e)
        finally:
            cursor.close()
            connection.close()
    return asistencias

def agregar_asistencia(estudiante_id, curso_id, fecha, estado):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Asistencias (EstudianteID, CursoID, Fecha, Estado) VALUES (?, ?, ?, ?)",
                (estudiante_id, curso_id, fecha, estado)
            )
            connection.commit()
        except Exception as e:
            print("Error al agregar asistencia:", e)
        finally:
            cursor.close()
            connection.close()

def actualizar_asistencia(asistencia_id, estudiante_id, curso_id, fecha, estado):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE Asistencias SET EstudianteID = ?, CursoID = ?, Fecha = ?, Estado = ? WHERE AsistenciaID = ?",
                (estudiante_id, curso_id, fecha, estado, asistencia_id)
            )
            connection.commit()
        except Exception as e:
            print("Error al actualizar asistencia:", e)
        finally:
            cursor.close()
            connection.close()

def eliminar_asistencia(asistencia_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Asistencias WHERE AsistenciaID = ?", (asistencia_id,))
            connection.commit()
        except Exception as e:
            print("Error al eliminar asistencia:", e)
        finally:
            cursor.close()
            connection.close()

def obtener_asistencia_por_id(asistencia_id):
    connection = get_db_connection()
    asistencia = None
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    a.AsistenciaID,
                    e.EstudianteID,
                    e.Nombre AS EstudianteNombre,
                    c.CursoID,
                    c.Nombre AS CursoNombre,
                    a.Fecha,
                    a.Estado
                FROM 
                    Asistencias a
                JOIN 
                    Estudiantes e ON a.EstudianteID = e.EstudianteID
                JOIN 
                    Cursos c ON a.CursoID = c.CursoID
                WHERE 
                    a.AsistenciaID = ?
            """, (asistencia_id,))
            row = cursor.fetchone()
            if row:
                asistencia = {
                    "AsistenciaID": row.AsistenciaID,
                    "EstudianteID": row.EstudianteID,
                    "EstudianteNombre": row.EstudianteNombre,
                    "CursoID": row.CursoID,
                    "CursoNombre": row.CursoNombre,
                    "Fecha": row.Fecha.isoformat() if hasattr(row.Fecha, 'isoformat') else row.Fecha,
                    "Estado": row.Estado
                }
        except Exception as e:
            print("Error al obtener asistencia por ID:", e)
        finally:
            cursor.close()
            connection.close()
    return asistencia


# modelS PARA USUARIOS


def obtener_usuarios():
    connection = get_db_connection()
    usuarios = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT UsuarioID, Nombre, Apellido, Email, Username, Rol, Estado, FechaCreacion, UltimoLogin
                FROM Usuarios
            """)
            usuarios = [
                {
                    "UsuarioID": row.UsuarioID,
                    "Nombre": row.Nombre,
                    "Apellido": row.Apellido,
                    "Email": row.Email,
                    "Username": row.Username,
                    "Rol": row.Rol,
                    "Estado": row.Estado,
                    "FechaCreacion": row.FechaCreacion.isoformat(),
                    "UltimoLogin": row.UltimoLogin.isoformat() if row.UltimoLogin else None
                }
                for row in cursor.fetchall()
            ]
        except Exception as e:
            print("Error al obtener usuarios:", e)
        finally:
            cursor.close()
            connection.close()
    return usuarios


import bcrypt
def agregar_usuario(nombre, apellido, email, username, password, rol):
    connection = get_db_connection()
    if connection:
        try:
            # Generar el hash de la contraseña
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Usuarios (Nombre, Apellido, Email, Username, PasswordHash, Rol)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, apellido, email, username, password_hash, rol))
            connection.commit()
        except Exception as e:
            print("Error al agregar usuario:", e)
        finally:
            cursor.close()
            connection.close()

def actualizar_usuario(usuario_id, nombre, apellido, email, username, rol, estado):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Usuarios
                SET Nombre = ?, Apellido = ?, Email = ?, Username = ?, Rol = ?, Estado = ?
                WHERE UsuarioID = ?
            """, (nombre, apellido, email, username, rol, estado, usuario_id))
            connection.commit()
        except Exception as e:
            print("Error al actualizar usuario:", e)
        finally:
            cursor.close()
            connection.close()

def eliminar_usuario(usuario_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Usuarios WHERE UsuarioID = ?", (usuario_id,))
            connection.commit()
        except Exception as e:
            print("Error al eliminar usuario:", e)
        finally:
            cursor.close()
            connection.close()

def obtener_usuario_por_id(usuario_id):
    connection = get_db_connection()
    usuario = None
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT UsuarioID, Nombre, Apellido, Email, Username, Rol, Estado, FechaCreacion, UltimoLogin
                FROM Usuarios
                WHERE UsuarioID = ?
            """, (usuario_id,))
            row = cursor.fetchone()
            if row:
                usuario = {
                    "UsuarioID": row.UsuarioID,
                    "Nombre": row.Nombre,
                    "Apellido": row.Apellido,
                    "Email": row.Email,
                    "Username": row.Username,
                    "Rol": row.Rol,
                    "Estado": row.Estado,
                    "FechaCreacion": row.FechaCreacion.isoformat(),
                    "UltimoLogin": row.UltimoLogin.isoformat() if row.UltimoLogin else None
                }
        except Exception as e:
            print("Error al obtener usuario por ID:", e)
        finally:
            cursor.close()
            connection.close()
    return usuario


# LOGIN
def validar_credenciales(username, password):
    connection = get_db_connection()
    usuario = None
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT UsuarioID, Username, PasswordHash, Rol, Nombre, Apellido
                FROM Usuarios 
                WHERE Username = ?
            """, (username,))
            row = cursor.fetchone()
            if row:
                hashed_password = row[2]  
                # Comparar la contraseña ingresada con el hash almacenado
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    usuario = {
                        "UsuarioID": row[0],  
                        "username": row[1],  
                        "rol": row[3],
                        "nombre": row[4],
                        "apellido": row[5]
                    }
        except Exception as e:
            print("Error al validar credenciales:", e)
        finally:
            cursor.close()
            connection.close()
    return usuario

#MODELS CURSOPROFESOR
def serialize_curso_profesor(row):
    return {
        "CursoID": row.CursoID,
        "Nombre": row.Nombre,
        "Descripcion": row.Descripcion,
        "Creditos": row.Creditos
    }

def serialize_curso_profesor_completo(row):
    return {
        "CursoID": row.CursoID,
        "CursoNombre": row.CursoNombre,
        "ProfesorID": row.ProfesorID,
        "ProfesorNombre": f"{row.ProfesorNombre} {row.ProfesorApellido}"
    }

def obtener_todos_cursos_profesores():
    """
    Obtiene todos los cursos y los profesores asignados.
    """
    connection = get_db_connection()
    cursos_profesores = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    c.CursoID, 
                    c.Nombre AS CursoNombre, 
                    p.ProfesorID, 
                    p.Nombre AS ProfesorNombre, 
                    p.Apellido AS ProfesorApellido
                FROM ProfesoresCursos pc
                INNER JOIN Cursos c ON pc.CursoID = c.CursoID
                INNER JOIN Profesores p ON pc.ProfesorID = p.ProfesorID
            """)
            records = cursor.fetchall()
            cursos_profesores = [serialize_curso_profesor_completo(row) for row in records]
        except Exception as e:
            print("Error al obtener todos los cursos y profesores:", e)
        finally:
            cursor.close()
            connection.close()
    return cursos_profesores


def obtener_cursos_por_profesor(profesor_id):
    """
    Obtiene los cursos asignados a un profesor mediante un procedimiento almacenado.
    """
    connection = get_db_connection()
    cursos = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("EXEC spObtenerCursosPorProfesor @ProfesorID = ?", (profesor_id,))
            records = cursor.fetchall()
            cursos = [serialize_curso_profesor(row) for row in records]
        except Exception as e:
            print("Error al obtener cursos por profesor:", e)
        finally:
            cursor.close()
            connection.close()
    return cursos

def asignar_curso_a_profesor(profesor_id, curso_id):
    """
    Asigna un curso a un profesor en la tabla ProfesoresCursos.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO ProfesoresCursos (ProfesorID, CursoID) VALUES (?, ?)",
                (profesor_id, curso_id)
            )
            connection.commit()
        except Exception as e:
            print("Error al asignar curso a profesor:", e)
        finally:
            cursor.close()
            connection.close()

def eliminar_curso_de_profesor(profesor_id, curso_id):
    """
    Elimina la relación entre un curso y un profesor.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM ProfesoresCursos WHERE ProfesorID = ? AND CursoID = ?",
                (profesor_id, curso_id)
            )
            connection.commit()
        except Exception as e:
            print("Error al eliminar curso de profesor:", e)
        finally:
            cursor.close()
            connection.close()

