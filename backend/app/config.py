import pyodbc
import os
from datetime import timedelta

# Configuración de la base de datos
def get_db_connection():
    try:
        connection = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=localhost\\SQLEXPRESS;"  # Nombre de tu servidor
    "Database=RegistroAcademicoColegio;"  # Nombre de la base de datos
    "Trusted_Connection=yes;"
)

        print("Conexión exitosa a la base de datos!")  
        return connection
    except Exception as e:
        print("Error de conexión:", e)
        return None

# Configuración de JWT
class Config:
    JWT_SECRET_KEY = 'potato123'  # Clave
    JWT_TOKEN_LOCATION = ['headers']  # Especifica las ubicaciones donde se puede buscar el token 
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)  # Establece la duración del token (12 horas)
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'potato123')  # Para sesiones, etc.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///mi_base_de_datos.db')  # Esto puede ser para SQLAlchemy si se usa
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Para evitar advertencias

