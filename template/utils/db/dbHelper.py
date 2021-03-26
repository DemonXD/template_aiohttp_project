#################################
# Date: 2021/03/25
# Author: Miles Xu
# Email: kanonxmm@163.com
# Desc.: 提供数据库控制层，包括不限于
#       - PostgreSQL
#       - Mysql
#       - MongoDB
#################################
# -*- coding: utf-8 -*-
import asyncpg
import aiomysql
import motor.motor_asyncio
from asyncpg.pool import Pool
from global_ import PublicManager
from .BaseHelper import BaseHelper


class PostgreSQLHelper(BaseHelper):
    _pool: Pool = None

    def __init__(self, db_config: dict) -> None:
        self.db_config = db_config

    async def connect(self):
        if self._pool is not None:
            pass
        else:
            PublicManager.logger.info(f"Connected to server({self.db_config['host']}/{self.db_config['database']}) successfully")
            self._pool = await asyncpg.create_pool(**self.db_config)


    @property
    def pool(self):
        return self._pool

    async def fetch(self, query):
        await self.connect()
        # Acquire a connection
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    result = await connection.fetch(query)
                except Exception as e:
                    PublicManager.logger.info(f"fetch ERROR:{e}")
                else:
                    return result

    # 使用fetch 获取数据样例
    #    sqls = """
    #    select * from devices_device where devicetype = 'agv';
    #    """
    #    devices = await PublicManager.dbpool.fetch(sqls)
    #    results = [{key: val for key, val in each_device.items()} for each_device in devices ]

    async def execute(self, sql, data):
        await self.connect()
        # Acquire a connection
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    exc_status = await connection.execute(sql, data)
                    PublicManager.logger.info(f"sql execute return: {exc_status}")
                except Exception as e:
                    PublicManager.logger.info(f"Store ERROR sql:{e}")

    async def close(self):
        await self._pool.close()


class MysqlHelper(BaseHelper):
    _pool = None

    def __init__(self, config):
        self.config = config


    async def connect(self):
        if self._pool is None:
            pool = await aiomysql.create_pool(**self.config)

            if pool:
                self._pool = pool
                PublicManager.logger.info("mysql connect success!!!")
                return self._pool
            else:
                raise("connect to mysql error ")
        else:
            return self._pool

    @property
    def pool(self):
        return self._pool


    async def query(self,query,args=None):
        await self.connect()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                (r,) = await cur.fetchone()
                assert r == 42

    async def close(self):
        """
            此方法提供在app.on_shutdown 中调用关闭
        """
        self._pool.close()
        await self._pool.wait_closed()


class MongoHelper(BaseHelper):
    _db = None
    def __init__(self, config) -> None:
        self.config = config

    @property
    def db(self):
        return self._db

    async def connect(self):
        if self._db is None:
            db = motor.motor_asyncio.AsyncIOMotorClient(self.config["url"])
            if db:
                self._db = db 
                PublicManager.logger.info("MongoDB connect success!!!")
            else:
                raise ("MongoDB connect failure!!!")

    async def do_find(self, collection, conditions):
        await self.connect()
        res = await self.db[collection].find(conditions).sort('i')
        return res
