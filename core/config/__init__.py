from functools import lru_cache
import os
from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

from .redis import RedisSettings
from .rabbitmq import RabbitMQSettings
from .minio import MINIOSettings
from .database import DBSettings

env_file = f".env{os.environ.get('ENV_FILE', '')}"


class Settings(BaseSettings):
    """项目配置文件设置"""
    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )

    APP_NAME: Literal["hzshield", "hzalarm", "hzoss"] = "hzshield"

    DB: DBSettings = DBSettings()
    MINIO: MINIOSettings = MINIOSettings()
    RABBITMQ: RabbitMQSettings = RabbitMQSettings()
    REDIS: RedisSettings = RedisSettings()

    JWT_SALT: str = "iv%x6xo7l7_u9bf_u!9#g#m*)*=ej@bek5)(@u3kh*72+unjv="
    TOKEN_DURATION: int = 999
    SERVER_ID: str = "1"
    
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    AUTH_SERVER: Optional[str] = None


@lru_cache
def get_settings() -> Settings:
    """获取全局配置"""
    return Settings()


# 创建配置实例
settings: Settings = get_settings()

__all__ = ["settings", "get_settings"]