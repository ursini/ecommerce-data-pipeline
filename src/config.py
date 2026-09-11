import os

from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def validate_config() -> None:
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL environment variable is not configured"
        )