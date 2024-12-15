from flask import Flask
from .config import get_db_connection
from .routes import main_routes, profesor_bp,curso_bp,inscripcion_bp,calificacion_bp,asistencia_bp,usuarios_bp,auth_bp,profesor_curso_bp
from flask_cors import CORS


app = Flask(__name__)

# Registrar el Blueprint
app.register_blueprint(main_routes)
app.register_blueprint(profesor_bp)
app.register_blueprint(curso_bp)
app.register_blueprint(inscripcion_bp)
app.register_blueprint(calificacion_bp)
app.register_blueprint(asistencia_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profesor_curso_bp)

CORS(app)  # Habilitar CORS
