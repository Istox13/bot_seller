from gino import Gino
from gino.schema import GinoSchemaVisitor

from tg_bot_seller.loader import config


db = Gino()


async def create_db():
    DB_USER = config.db_config.user
    DB_PASS = config.db_config.password
    DB_HOST = config.db_config.host
    DB_NAME = config.db_config.db_name
    DB_PORT = config.db_config.port

    await db.set_bind(f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    db.gino: GinoSchemaVisitor
    await db.gino.create_all()
