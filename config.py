from starlette.config import Config
import asyncpg
import databases
from databases import DatabaseURL

config = Config(".env")

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=str)
POSTGRES_PORT = config("POSTGRES_PORT", cast=int)
POSTGRES_DB = config("POSTGRES_DB", cast=str)
POSTGRES_SERVER = config("POSTGRES_SERVER")


async def get_db_connection():
    return await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB,
        host=POSTGRES_SERVER,
        port=POSTGRES_PORT
    )