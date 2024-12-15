from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config  
from app import app   

# Crear la instancia de Flask
app = Flask(__name__)

# Cargar la configuración desde config.py
app.config.from_object(Config)

# Inicializar JWTManager
jwt = JWTManager(app)

# Habilitar CORS
CORS(app)

# Registrar los Blueprints de las rutas
from app.routes import main_routes, profesor_bp, curso_bp, inscripcion_bp, calificacion_bp, asistencia_bp, usuarios_bp, auth_bp,profesor_curso_bp
app.register_blueprint(main_routes)
app.register_blueprint(profesor_bp)
app.register_blueprint(curso_bp)
app.register_blueprint(inscripcion_bp)
app.register_blueprint(calificacion_bp)
app.register_blueprint(asistencia_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profesor_curso_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
