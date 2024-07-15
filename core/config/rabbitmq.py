from pydantic import BaseModel


class RabbitMQSettings(BaseModel):
    """消息队列配置"""

    HOST: str = "rabbitmq"
    PORT: int = 5672
    USER: str = "root"
    PASSWORD: str = "root"

    @property
    def RABBITMQ(self):
        return f"amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}"

    def rabbitmq_with_vhost(self, vhost: str):
        return self.RABBITMQ + vhost