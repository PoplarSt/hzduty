

from .mysql import Mysql


class DBRegistry(type):
    """数据库初始化类"""

    _models = {}

    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        if new_class.__name__ != "HZDB":
            cls._models[new_class.__db_name__] = new_class
        return new_class


class HZDB(metaclass=DBRegistry):
    _instance = None
    __db_name__ = "default"
    DATABASES = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls.DATABASES[cls.__db_name__]

    @classmethod
    async def session(cls):
        db_session = cls.DATABASES[cls.__db_name__].SessionLocal()
        try:
            yield db_session
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            raise e
        finally:
            await db_session.close()


    def __init__(self, config) -> None:
        """"""
        self.__parse_config(config)


    def __parse_config(self, config) -> None:
        """解析配置文件"""
        print(self.__class__._models)
        for name, db_config in config.items():
            db = self.get_db(db_config)
            self.DATABASES[name] = db


    def get_db(self, db_config):
        """获取数据库"""
        if db_config["TYPE"] == "mysql":
            return Mysql(db_config)
        # if db_config["type"].lower() == "dameng":
        #     return Dameng(db_config)
        # if db_config["type"].lower() == "postgresql":
        #     return PostgreSQL(db_config)
        else:
            raise ValueError("数据库类型不支持")


    def reconnect(self) -> None:
        for _, db in self.databases.items():
            if isinstance(db, Mysql):
                db.reconnect()


    def has_db(self, name) -> bool:
        return name in self.databases.keys()