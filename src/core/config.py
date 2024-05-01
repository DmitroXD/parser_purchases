from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    # Env Bot
    BOT_TOKEN: str
    REDIS_PATH: str | None = None  # Example "redis://root:@localhost:6379"
    BOT_WEBHOOK_URL: str | None = None

    # Env Middleware
    ADMIN_MIDDLEWARE: bool = False

    # Env Mysql
    MYSQL_PATH: str = "sqlite://:memory:"  # Example "mysql://root:root@localhost:3306"

    # Env Rusprofile
    RUS_PROFILE_LOGIN: str
    RUS_PROFILE_PASSWORD: str

    # Env system
    ENCODING: str = "utf-8"
    USER_AGENT: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"

    # Env Admin
    DEVELOPER_ID: int
    ADMINISTRATOR_ID: int


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
