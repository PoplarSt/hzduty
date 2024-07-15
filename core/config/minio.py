from pydantic import BaseModel
from urllib.parse import quote_plus as urlquote


class MINIOSettings(BaseModel):
    """消息队列配置"""

    HOST: str = ""
    ENDPOINT: str = "minio:9000"
    ACCESS_KEY: str = "root"
    SECRET_KEY: str = "root"
    SECURE: bool = False
    PREFIX: str = ""
    BUCKET: str | list[str] = "file"

    @property
    def URL(self):
        return f"redis://{self.USER}:{urlquote(self.PASSWORD)}@{self.HOST}:{self.PORT}/{self.DB}"