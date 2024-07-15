import ujson


from .meta import RelationalDatabase

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus as urlquote


class Mysql(RelationalDatabase):
    def __init__(self, db_config) -> None:
        self.__pool = None  # 连接池对象
        db_config = dict(filter(lambda x: x[0] != "type", db_config.items()))
        # self.__get_pool(db_config)
        self.user = db_config.get("USER")
        self.password = db_config.get("PASSWORD")
        self.host = db_config.get("HOST")
        self.port = db_config.get("PORT")
        self.database = db_config.get("DATABASE")
        self.charset = db_config.get("CHARSET")
        self.echo = db_config.get("ECHO", False)

        self.uri = f"mysql+aiomysql://{self.user}:{urlquote(self.password)}@{self.host}:{self.port}/{self.database}?charset={self.charset}"
        self.sync_uri = f"mysql+pymysql://{self.user}:{urlquote(self.password)}@{self.host}:{self.port}/{self.database}?charset={self.charset}"
        self.create_session()
        # self.DB_URI = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?charset={self.charset}"
        # self.sync_engine = create_engine(
        #     self.sync_uri,
        #     echo=self.echo,
        #     pool_size=10,
        #     max_overflow=5,
        #     pool_reset_on_return=None,
        #     pool_pre_ping=True,
        #     json_serializer=lambda v: ujson.dumps(v, ensure_ascii=False),
        #     json_deserializer=lambda v: ujson.loads(v),
        # )
        # self.syncSessionLocal = sessionmaker(
        #     bind=self.sync_engine,
        #     autoflush=False,
        #     autocommit=False,
        #     expire_on_commit=False,
        # )

        # self.engine = create_async_engine(
        #     self.uri,
        #     echo=self.echo,
        #     future=True,
        #     pool_size=10,
        #     max_overflow=5,
        #     pool_recycle=3600,
        #     pool_reset_on_return=None,
        #     pool_pre_ping=True,
        #     json_serializer=lambda v: ujson.dumps(v, ensure_ascii=False),
        #     json_deserializer=lambda v: ujson.loads(v),
        #     # poolclass=NullPool,
        # )
        # self.SessionLocal = async_sessionmaker(
        #     class_=AsyncSession,
        #     bind=self.engine,
        #     autoflush=False,
        #     autocommit=False,
        #     expire_on_commit=False,
        # )

        # self.Base.metadata.create_all(self.engine)

        # metadata = self.Base.metadata
        # metadata.bind = self.engine

    # def __get_pool(self, db_config):
    #     # __pool = await aiomysql.create_pool(
    #     #     host=self.host,
    #     #     port=self.port,
    #     #     user=self.user,
    #     #     password=self.password,
    #     #     db=self.database,
    #     # )
    #     __pool = PooledDB(
    #         creator=pymysql,  # 使用链接数据库的模块
    #         maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    #         mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    #         maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    #         maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    #         blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    #         maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    #         setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    #         ping=0,  # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    #         **db_config,
    #     )
    #     self.__pool = __pool
    def create_session(self):
        print(f"开始连接数据库：{self.database}")
        self.sync_engine = create_engine(
            self.sync_uri,
            echo=self.echo,
            pool_size=10,
            max_overflow=5,
            pool_reset_on_return=None,
            pool_pre_ping=True,
            json_serializer=lambda v: ujson.dumps(v, ensure_ascii=False),
            json_deserializer=lambda v: ujson.loads(v),
        )
        self.syncSessionLocal = sessionmaker(
            bind=self.sync_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

        self.engine = create_async_engine(
            self.uri,
            echo=self.echo,
            future=True,
            pool_size=10,
            max_overflow=5,
            pool_reset_on_return=None,
            pool_pre_ping=True,
            json_serializer=lambda v: ujson.dumps(v, ensure_ascii=False),
            json_deserializer=lambda v: ujson.loads(v),
            # poolclass=NullPool,
        )
        self.SessionLocal = async_sessionmaker(
            class_=AsyncSession,
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
    def reconnect(self):
        return self.create_session()
    # def get_cursor(self):
    #     pass
    #     # conn = self.__pool.connection()
    #     # cursor = conn.cursor(pymysql.cursors.SSDictCursor)
    #     # return conn, cursor

    # def execute(self, sql, params=None):
    #     with self.syncSessionLocal() as db_session:
    #         r = db_session.execute(text(sql), params)
    #         return r

    # async def async_execute(self, sql: str, params=None):
    #     async with self.engine.connect() as conn:
    #         r = await conn.execute(text(sql), params)
    #         await conn.commit()
    #         return r

    # # def execute_many(self, sql, params=None):
    # #     return super().execute_many(sql, params)

    # def fetchone(self, sql, params=None):
    #     with self.syncSessionLocal() as db_session:
    #         r = db_session.execute(text(sql), params)
    #         return r.mappings().one()

    # def query(self, sql, params=None) -> None:
    #     with self.syncSessionLocal() as db_session:
    #         r = db_session.execute(text(sql), params)
    #         return r.mappings().all()
    #     # conn, cursor = self.get_cursor()
    #     # cursor.execute(sql, params)
    #     # result = cursor.fetchall() or []
    #     # # logger.info(cursor._last_executed)
    #     # cursor.close()
    #     # conn.close()
    #     # return result

    # async def connection(self):
    #     async with self.engine.begin() as connection:
    #         yield connection

    # async def session(self):
    #     # async with self.SessionLocal() as session:
    #     #     try:
    #     #         yield session
    #     #         await session.commit()
    #     #     except IntegrityError as e:
    #     #         print(e)
    #     #         # error_code, error_message = e.args
    #     #         # if error_code == 1062:
    #     #         #     print("该数据已存在，请不要重复插入")
    #     #         # else:
    #     #         #     print(f"发生了IntegrityError，错误码为{error_code}，错误信息为{error_message}")
    #     #         await session.rollback()
    #     #     except Exception as e:
    #     #         print("Exception", e)
    #     #         await session.rollback()
    #     # finally:
    #     #     await session.close()

    #     db: AsyncSession = self.SessionLocal()

    #     # yield db
    #     # await db.commit()
    #     # await db.close()
    #     try:
    #         yield db
    #         await db.commit()
    #     # except IntegrityError as e:
    #     #     # print(e)
    #     #     # error_code, error_message = e.args
    #     #     # if error_code == 1062:
    #     #     #     print("该数据已存在，请不要重复插入")
    #     #     # else:
    #     #     #     print(f"发生了IntegrityError，错误码为{error_code}，错误信息为{error_message}")
    #     #     await db.rollback()
    #     #     raise e
    #     except Exception as e:
    #         # print("Exception", e)
    #         await db.rollback()
    #         raise e
    #     finally:
    #         await db.close()

    # async def async_query(self, sql: SQLParser | str, params: dict = None):
    #     async with self.SessionLocal() as db_session:
    #         if isinstance(sql, str):
    #             q = await db_session.execute(text(sql), params)
    #         else:
    #             q = await db_session.execute(text(str(sql)), sql.dict())
    #         return q.mappings().all()

    # async def async_get(self, sql: SQLParser | str, params: dict = None):
    #     async with self.SessionLocal() as db_session:
    #         if isinstance(sql, str):
    #             q = await db_session.execute(text(sql), params)
    #         else:
    #             q = await db_session.execute(text(str(sql)), sql.dict())
    #         return q.mappings().one_or_none()

    # async def orm_execute(self, sql):
    #     async with self.SessionLocal() as db_session:
    #         async with db_session.begin():
    #             r = await db_session.execute(sql)
    #         await db_session.commit()
    #     return r
