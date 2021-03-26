from global_ import PubManager
import os
import logging
import logging.handlers
import pathlib

from asyncpg.exceptions import AssertError
from utils.db import DBSelector
from utils.db import redisHelper
from utils.mqtt.mqttHelper import MQTTSubscriber


def init_log(PublicManager):
    PublicManager.conf.read_log()
    PublicManager.logger=logging.getLogger()
    PublicManager.logger.setLevel(PublicManager.conf.level)
    log_info_file = os.path.join(PublicManager.conf.filepath, PublicManager.conf.logname_info)
    log_error_file = os.path.join(PublicManager.conf.filepath, PublicManager.conf.logname_error)
    if not os.path.exists(PublicManager.conf.filepath):
        os.makedirs(PublicManager.conf.filepath)
    if not os.path.exists(log_info_file):
       pathlib.Path(log_info_file).touch()
    if not os.path.exists(log_error_file):
       pathlib.Path(log_error_file).touch()
    
    # file log handler hold ERROR log
    fh_error = logging.handlers.TimedRotatingFileHandler(
        log_error_file,
        when = 'D',
        # maxBytes=10*1024*1024,
        backupCount = 7 # max 7 days log files
    )
    fh_error.setLevel(logging.ERROR)

    # file log handler hold ERROR log
    fh_info = logging.handlers.TimedRotatingFileHandler(
        log_info_file,
        when = 'D',
        # maxBytes=10*1024*1024,
        backupCount = 7 # max 7 days log files
    )
    fh_info.setLevel(logging.INFO)

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(module)s:%(filename)s:[lineno]:%(lineno)s - L%(levelname)s:%(message)s')
    fh_error.setFormatter(formatter)
    fh_info.setFormatter(formatter)
    sh.setFormatter(formatter)
    PublicManager.logger.addHandler(sh)
    PublicManager.logger.addHandler(fh_error)
    PublicManager.logger.addHandler(fh_info)


async def init_dbpool(PublicManager, name, typ="postgresql"):
    # read_db 可以指定数据库种类，默认是PostgreSQL
    db_config: dict = PublicManager.conf.read_db(typ)
    try:
        # 返回的是数据库连接对象
        PublicManager.dbpool[name] = DBSelector.initDB(typ, db_config)
        assert PublicManager.dbpool[name] is not None, "db[{0}] init failure".format(name)
        # 使用:
        # PublicManager.dbpool[name].fetch(sql)
    except AssertError as e:
        PublicManager.logger.error(str(e))
    

def init_mqtt(PublicManager):
    mqtt_conf = PublicManager.conf.read_mqtt()
    PublicManager.mqttclient = MQTTSubscriber()
    PublicManager.mqttclient.start(**mqtt_conf)


async def init_redis(PublicManager):
    redis_conf = PublicManager.conf.read_redis()
    PublicManager.redisdb = redisHelper(redis_conf)
