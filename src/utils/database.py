import psycopg2

from src.config import DATABASE_URL, validate_config


def get_connection():
    validate_config()

    return psycopg2.connect(DATABASE_URL)