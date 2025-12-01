import os

# Caminho raiz das imagens
IMAGE_ROOT_PATH = os.getenv("IMAGE_ROOT_VOLUME_PATH", "/app/ML/dataset/iot/")
if IMAGE_ROOT_PATH and not IMAGE_ROOT_PATH.endswith(os.sep):
    IMAGE_ROOT_PATH += os.sep

# CORS
CORS_ORIGINS = ["http://localhost:8080", "http://127.0.0.1:8080", "*"]

# Banco de Dados
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")
DB_NAME = os.getenv("POSTGRES_DB", "demeter")