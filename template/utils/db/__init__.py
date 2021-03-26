from .dbHelper import PostgreSQLHelper, MysqlHelper, MongoHelper
from .redisHelper import redisHelper


__all__ = [
    "PostgreSQLHelper",
    "MysqlHelper",
    "MongoHelper",
    "redisHelper"
]


class DBSelector:
    db_map = {
        "postgresql": PostgreSQLHelper,
        "mysql": MysqlHelper,
        "mongo": MongoHelper
    }
    @staticmethod
    def initDB(typ, config):
        return DBSelector.db_map.get(typ)(config)


