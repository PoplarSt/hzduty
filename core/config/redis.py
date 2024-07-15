from pydantic import BaseModel
from urllib.parse import quote_plus as urlquote


class RedisSettings(BaseModel):
    """消息队列配置"""

    HOST: str = "redis"
    PORT: int = 6379
    USER: str = "root"
    PASSWORD: str = "root"
    DB: int = 0

    @property
    def URL(self):
        return f"redis://{self.USER}:{urlquote(self.PASSWORD)}@{self.HOST}:{self.PORT}/{self.DB}"