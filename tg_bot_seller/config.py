from dataclasses import dataclass

from environs import Env


@dataclass
class BotConfig:
    token: str
    admin_id: int
    admin_password: str


@dataclass
class DBConfig:
    host: str
    port: str
    user: str
    password: str
    db_name: str


@dataclass
class Config:
    bot_config: BotConfig
    db_config: DBConfig


def get_config() -> Config:
    env = Env()

    env.read_env()

    return Config(
        bot_config=BotConfig(
            token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            admin_password=env.str("ADMIN_PASS")
        ),
        db_config=DBConfig(
            host=env.str("DB_HOST"),
            port=env.str("DB_PORT"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASS"),
            db_name=env.str("DB_NAME")
        )
    )
