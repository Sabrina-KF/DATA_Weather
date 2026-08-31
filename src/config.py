import os
from dotenv import load_dotenv

load_dotenv()

# Localisation : Tours, France
LATITUDE = 47.3941
LONGITUDE = 0.6848

# Base de données
POSTGRES_USER = os.getenv("POSTGRES_USER", "weather_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "weather_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "weather_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")


def get_database_url() -> str:
    return (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )