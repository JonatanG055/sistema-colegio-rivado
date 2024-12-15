from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager, create_access_token
from app.models import (
    obtener_estudiantes,
    agregar_estudiante,
    actualizar_estudiante,
    eliminar_estudiante,
    obtener_estudiante_por_id,
    validar_credenciales,
    obtener_profesores, agregar_profesor, actualizar_profesor, eliminar_profesor, obtener_profesor_por_id,
    obtener_cursos, agregar_curso, actualizar_curso, eliminar_curso_db, obtener_curso_por_id,
    obtener_inscripciones, agregar_inscripcion, actualizar_inscripcion, eliminar_inscripcion, obtener_inscripcion_por_id, obtener_cursos_por_estudiante_id,
    obtener_calificaciones, agregar_calificacion, actualizar_calificacion, eliminar_calificacion, obtener_calificacion_por_id,
    obtener_asistencias, agregar_asistencia, actualizar_asistencia, eliminar_asistencia, obtener_asistencia_por_id,
    obtener_usuarios, agregar_usuario, actualizar_usuario, eliminar_usuario, obtener_usuario_por_id,
    validar_credenciales ,obtener_cursos_por_profesor, asignar_curso_a_profesor, eliminar_curso_de_profesor, obtener_todos_cursos_profesores
)
from app.config import get_db_connection  

# Crear Blueprint para las rutas principales
main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return "Bienvenido a la aplicación de CRUD"

@main_routes.route('/check_db')
def check_db():
    conn = get_db_connection()
    if conn:
        print("Conexión exitosa a la base de datos!")
        conn.close()
        return "Conexión exitosa a la base de datos!"
    else:
        print("Fallo en la conexión a la base de datos.")
        return "Fallo en la conexión a la base de datos.", 500  

@main_routes.route('/api/estudiantes', methods=['GET'])
@jwt_required()
def get_estudiantes():
    estudiantes = obtener_estudiantes()
    return jsonify(estudiantes), 200  

@main_routes.route('/api/estudiantes', methods=['POST'])
@jwt_required()
def add_estudiante():
    data = request.get_json()
    if not data or not all(key in data for key in ('nombre', 'apellido', 'fecha_nacimiento', 'direccion', 'telefono', 'email')):
        return jsonify({"message": "Datos incompletos"}), 400  
    agregar_estudiante(data['nombre'], data['apellido'], data['fecha_nacimiento'], data['direccion'], data['telefono'], data['email'])
    return jsonify({"message": "Estudiante agregado exitosamente", "data": data}), 201 

@main_routes.route('/api/estudiantes/<int:estudiante_id>', methods=['GET'])
@jwt_required()
def get_estudiante(estudiante_id):
    estudiante = obtener_estudiante_por_id(estudiante_id)
    if estudiante:
        return jsonify(estudiante), 200  
    else:
        return jsonify({"message": "Estudiante no encontrado"}), 404  

@main_routes.route('/api/estudiantes/<int:estudiante_id>', methods=['PUT'])
@jwt_required()
def edit_estudiante(estudiante_id):
    data = request.get_json()
    if not data or not all(key in data for key in ('nombre', 'apellido', 'fecha_nacimiento', 'direccion', 'telefono', 'email')):
        return jsonify({"message": "Datos incompletos"}), 400  
    actualizar_estudiante(estudiante_id, data['nombre'], data['apellido'], data['fecha_nacimiento'], data['direccion'], data['telefono'], data['email'])
    return jsonify({"message": "Estudiante actualizado exitosamente"}), 200  

@main_routes.route('/api/estudiantes/<int:estudiante_id>', methods=['DELETE'])
@jwt_required()
def delete_estudiante(estudiante_id):
    eliminar_estudiante(estudiante_id)
    return jsonify({"message": "Estudiante eliminado exitosamente"}), 200  

# Rutas para profesores
profesor_bp = Blueprint('profesores', __name__)

@profesor_bp.route('/profesores', methods=['GET'])
@jwt_required()
def listar_profesores():
    profesores = obtener_profesores()
    return jsonify(profesores), 200

@profesor_bp.route('/profesores', methods=['POST'])
@jwt_required()
def crear_profesor():
    data = request.json
    agregar_profesor(data['Nombre'], data['Apellido'], data['Especialidad'], data['Telefono'], data['Email'])
    return jsonify({"message": "Profesor agregado exitosamente"}), 201

@profesor_bp.route('/profesores/<int:profesor_id>', methods=['PUT'])
@jwt_required()
def modificar_profesor(profesor_id):
    data = request.json
    actualizar_profesor(profesor_id, data['Nombre'], data['Apellido'], data['Especialidad'], data['Telefono'], data['Email'])
    return jsonify({"message": "Profesor actualizado exitosamente"}), 200

@profesor_bp.route('/profesores/<int:profesor_id>', methods=['DELETE'])
@jwt_required()
def eliminar_profesor_route(profesor_id):
    eliminar_profesor(profesor_id)
    return jsonify({"message": "Profesor eliminado exitosamente"}), 200

@profesor_bp.route('/profesores/<int:profesor_id>', methods=['GET'])
@jwt_required()
def obtener_profesor(profesor_id):
    profesor = obtener_profesor_por_id(profesor_id)
    return jsonify(profesor), 200 if profesor else 404

# Rutas para cursos
curso_bp = Blueprint('cursos', __name__)

@curso_bp.route('/cursos', methods=['GET'])
@jwt_required()
def listar_cursos():
    cursos = obtener_cursos()
    return jsonify(cursos), 200

@curso_bp.route('/cursos', methods=['POST'])
@jwt_required()
def crear_curso():
    data = request.json
    agregar_curso(data['Nombre'], data['Descripcion'], data['Creditos'])
    return jsonify({"message": "Curso agregado exitosamente"}), 201

@curso_bp.route('/cursos/<int:curso_id>', methods=['PUT'])
@jwt_required()
def modificar_curso(curso_id):
    data = request.json
    actualizar_curso(curso_id, data['Nombre'], data['Descripcion'], data['Creditos'])
    return jsonify({"message": "Curso actualizado exitosamente"}), 200

@curso_bp.route('/cursos/<int:curso_id>', methods=['DELETE'])
@jwt_required()
def eliminar_curso_route(curso_id):
    eliminar_curso_db(curso_id)
    return jsonify({"message": "Curso eliminado exitosamente"}), 200

@curso_bp.route('/cursos/<int:curso_id>', methods=['GET'])
@jwt_required()
def obtener_curso(curso_id):
    curso = obtener_curso_por_id(curso_id)
    return jsonify(curso), 200 if curso else 404



# Rutas para inscripciones
inscripcion_bp = Blueprint('inscripciones', __name__)

@inscripcion_bp.route('/inscripciones', methods=['GET'])
@jwt_required()
def listar_inscripciones():
    inscripciones = obtener_inscripciones()
    return jsonify(inscripciones), 200

@inscripcion_bp.route('/inscripciones', methods=['POST'])
@jwt_required()
def crear_inscripcion():
    data = request.json
    agregar_inscripcion(data['EstudianteID'], data['CursoID'], data['FechaInscripcion'])
    return jsonify({"message": "Inscripción agregada exitosamente"}), 201

@inscripcion_bp.route('/inscripciones/<int:inscripcion_id>', methods=['PUT'])
@jwt_required()
def modificar_inscripcion(inscripcion_id):
    data = request.json
    actualizar_inscripcion(inscripcion_id, data['EstudianteID'], data['CursoID'], data['FechaInscripcion'])
    return jsonify({"message": "Inscripción actualizada exitosamente"}), 200

@inscripcion_bp.route('/inscripciones/<int:inscripcion_id>', methods=['DELETE'])
@jwt_required()
def eliminar_inscripcion_route(inscripcion_id):
    eliminar_inscripcion(inscripcion_id)
    return jsonify({"message": "Inscripción eliminada exitosamente"}), 200

@inscripcion_bp.route('/inscripciones/<int:inscripcion_id>', methods=['GET'])
@jwt_required()
def obtener_inscripcion(inscripcion_id):
    inscripcion = obtener_inscripcion_por_id(inscripcion_id)
    return jsonify(inscripcion), 200 if inscripcion else 404

# Ruta para obtener cursos inscritos por un estudiante
@inscripcion_bp.route('/inscripciones/estudiantes/<int:estudiante_id>/cursos', methods=['GET'])
@jwt_required()
def obtener_cursos_inscritos(estudiante_id):
    cursos = obtener_cursos_por_estudiante_id(estudiante_id)
    if cursos:
        return jsonify(cursos), 200
    else:
        return jsonify({"message": "No se encontraron cursos para el estudiante"}), 404

# Rutas para calificaciones
calificacion_bp = Blueprint('calificaciones', __name__)

@calificacion_bp.route('/calificaciones', methods=['GET'])
@jwt_required()
def listar_calificaciones():
    calificaciones = obtener_calificaciones()
    return jsonify(calificaciones), 200

@calificacion_bp.route('/calificaciones', methods=['POST'])
@jwt_required()
def crear_calificacion():
    data = request.json
    agregar_calificacion(data['EstudianteID'], data['CursoID'], data['Nota'])
    return jsonify({"message": "Calificación agregada exitosamente"}), 201

@calificacion_bp.route('/calificaciones/<int:calificacion_id>', methods=['PUT'])
@jwt_required()
def modificar_calificacion(calificacion_id):
    data = request.json
    actualizar_calificacion(calificacion_id, data['EstudianteID'], data['CursoID'], data['Nota'])
    return jsonify({"message": "Calificación actualizada exitosamente"}), 200
    

@calificacion_bp.route('/calificaciones/<int:calificacion_id>', methods=['DELETE'])
@jwt_required()
def eliminar_calificacion_route(calificacion_id):
    eliminar_calificacion(calificacion_id)
    return jsonify({"message": "Calificación eliminada exitosamente"}), 200

@calificacion_bp.route('/calificaciones/<int:calificacion_id>', methods=['GET'])
@jwt_required()
def obtener_calificacion(calificacion_id):
    calificacion = obtener_calificacion_por_id(calificacion_id)
    return jsonify(calificacion), 200 if calificacion else 404



#ROUTES ASITENCIAS 
from app.models import obtener_asistencias, agregar_asistencia, actualizar_asistencia, eliminar_asistencia, obtener_asistencia_por_id

asistencia_bp = Blueprint('asistencias', __name__)

@asistencia_bp.route('/asistencias', methods=['GET'])
@jwt_required()
def listar_asistencias():
    asistencias = obtener_asistencias()
    return jsonify(asistencias), 200

@asistencia_bp.route('/asistencias', methods=['POST'])
@jwt_required()
def crear_asistencia():
    data = request.json
    if 'EstudianteID' not in data or 'CursoID' not in data or 'Fecha' not in data or 'Estado' not in data:
        return jsonify({"error": "Datos incompletos"}), 400
    agregar_asistencia(data['EstudianteID'], data['CursoID'], data['Fecha'], data['Estado'])
    return jsonify({"message": "Asistencia agregada exitosamente"}), 201

@asistencia_bp.route('/asistencias/<int:asistencia_id>', methods=['PUT'])
@jwt_required()
def modificar_asistencia(asistencia_id):
    data = request.json
    if 'EstudianteID' not in data or 'CursoID' not in data or 'Fecha' not in data or 'Estado' not in data:
        return jsonify({"error": "Datos incompletos"}), 400
    actualizar_asistencia(asistencia_id, data['EstudianteID'], data['CursoID'], data['Fecha'], data['Estado'])
    return jsonify({"message": "Asistencia actualizada exitosamente"}), 200

@asistencia_bp.route('/asistencias/<int:asistencia_id>', methods=['DELETE'])
@jwt_required()
def eliminar_asistencia_route(asistencia_id):
    eliminar_asistencia(asistencia_id)
    return jsonify({"message": "Asistencia eliminada exitosamente"}), 200

@asistencia_bp.route('/asistencias/<int:asistencia_id>', methods=['GET'])
@jwt_required()
def obtener_asistencia(asistencia_id):
    asistencia = obtener_asistencia_por_id(asistencia_id)
    return jsonify(asistencia), 200 if asistencia else (jsonify({"error": "Asistencia no encontrada"}), 404)

#RUTAS PARA USUAIROS


# routes.py

from app.models import obtener_usuarios, agregar_usuario, actualizar_usuario, eliminar_usuario, obtener_usuario_por_id

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['GET'])
@jwt_required()
def listar_usuarios():
    usuarios = obtener_usuarios()
    return jsonify(usuarios), 200

@usuarios_bp.route('/usuarios', methods=['POST'])
#@jwt_required() DESHABILITADO 
def crear_usuario():
    data = request.json
    if not all(key in data for key in ('Nombre', 'Apellido', 'Email', 'Username', 'PasswordHash', 'Rol')):
        return jsonify({"error": "Datos incompletos"}), 400
    agregar_usuario(data['Nombre'], data['Apellido'], data['Email'], data['Username'], data['PasswordHash'], data['Rol'])
    return jsonify({"message": "Usuario creado exitosamente"}), 201

@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def modificar_usuario(usuario_id):
    data = request.json
    if not all(key in data for key in ('Nombre', 'Apellido', 'Email', 'Username', 'Rol', 'Estado')):
        return jsonify({"error": "Datos incompletos"}), 400
    actualizar_usuario(usuario_id, data['Nombre'], data['Apellido'], data['Email'], data['Username'], data['Rol'], data['Estado'])
    return jsonify({"message": "Usuario actualizado exitosamente"}), 200

@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
def eliminar_usuario_route(usuario_id):
    eliminar_usuario(usuario_id)
    return jsonify({"message": "Usuario eliminado exitosamente"}), 200

@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
@jwt_required()
def obtener_usuario(usuario_id):
    usuario = obtener_usuario_por_id(usuario_id)
    return jsonify(usuario), 200 if usuario else (jsonify({"error": "Usuario no encontrado"}), 404)



auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Faltan datos de inicio de sesión"}), 400

    usuario = validar_credenciales(username, password)
    if usuario:
        access_token = create_access_token(identity=str(usuario['UsuarioID'])) 
        return jsonify({
            "message": "Inicio de sesión exitoso", 
            "access_token": access_token,
            "usuario": {
                "UsuarioID": usuario['UsuarioID'],
                "username": usuario['username'],
                "rol": usuario['rol'],
                "nombre": usuario['nombre'],
                "apellido": usuario['apellido'],
            }
        }), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401
    

#ROUTES CURSOPROFESOR
# Crear Blueprint
profesor_curso_bp = Blueprint('profesores_cursos', __name__)

@profesor_curso_bp.route('/profesores/<int:profesor_id>/cursos', methods=['GET'])
@jwt_required()
def listar_cursos_por_profesor(profesor_id):
    """
    Lista todos los cursos asignados a un profesor específico.
    """
    cursos = obtener_cursos_por_profesor(profesor_id)
    return jsonify(cursos), 200 if cursos else 404

@profesor_curso_bp.route('/profesores/<int:profesor_id>/cursos', methods=['POST'])
@jwt_required()
def asignar_curso(profesor_id):
    """
    Asigna un curso a un profesor.
    """
    data = request.json
    curso_id = data.get('CursoID')
    if not curso_id:
        return jsonify({"error": "CursoID es requerido"}), 400
    asignar_curso_a_profesor(profesor_id, curso_id)
    return jsonify({"message": "Curso asignado exitosamente"}), 201

@profesor_curso_bp.route('/profesores/<int:profesor_id>/cursos/<int:curso_id>', methods=['DELETE'])
@jwt_required()
def eliminar_curso(profesor_id, curso_id):
    """
    Elimina la relación entre un curso y un profesor.
    """
    eliminar_curso_de_profesor(profesor_id, curso_id)
    return jsonify({"message": "Curso eliminado exitosamente"}), 200

@profesor_curso_bp.route('/profesores/cursos', methods=['GET'])
@jwt_required()
def listar_todos_cursos_profesores():
    """
    Lista todos los cursos junto con los profesores asignados.
    """
    cursos_profesores = obtener_todos_cursos_profesores()
    return jsonify(cursos_profesores), 200 if cursos_profesores else 404
