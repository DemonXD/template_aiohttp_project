#################################
# Date: 2021/03/25
# Author: Miles Xu
# Email: kanonxmm@163.com
# Desc.: 提供reids的control层
#################################
# -*- coding: utf-8 -*-
import aioredis
from .BaseHelper import BaseHelper
from global_.PubManager import PublicManager


class redisHelper(BaseHelper):
    _pool = None
    # loop = asyncio.get_running_loop()
    def __init__(self, config) -> None:
        self.config = config

    async def connect(self):
        if self._pool is  None:
            db = await aioredis.create_pool(
                (self.config["host"], self.config["port"]),
                db=self.config["db"],
                password=self.config["password"]
            )
            if db:
                self._pool = db
                PublicManager.logger.info("redis connect success!!!") 
            else:
                raise ("redis connect failure!!!")

    async def set_key(self, key, value):
        await self.connect()
        with await self._pool as db:
            await db.set(key, value)

    async def read_key(self, key):
        await self.connect()
        with await self._pool as db:
            res = await db.get(key)
        return res

    async def close(self):
        self._pool.close()
    
    def __del__(self):
        self._pool.close()