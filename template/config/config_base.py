from ruamel.yaml import YAML

class Config:
    yaml = YAML(typ="safe")
    def __init__(self, filename, typ="test"):
        self.filename = filename
        self.config = self.load_config(filename, typ)

    def load_config(self, filename, typ):
        with open(filename, "r", encoding="utf8") as f:
            config = self.yaml.load(f)
        return config[typ]

    def check_db_type(self, typ):
        if self.config.get(typ, None) is not None:
            return typ
        return

    def read_log(self):
        self.level = self.config.get("log").get("level")
        self.filepath = self.config.get("log").get("filepath")
        self.logname_info = self.config.get("log").get("logname_info")
        self.logname_error = self.config.get("log").get("logname_error")

    def read_master(self):
        self.host = self.config.get("master").get("ip")
        self.port = self.config.get("master").get("port")

    def read_mqtt(self):
        return {
            "host" : self.config.get("mqtt").get("host"),
            "port" : self.config.get("mqtt").get("port"),
            "topic" : self.config.get("mqtt").get("topic"),
            "username" : self.config.get("mqtt").get("username"),
            "password" : self.config.get("mqtt").get("password")
        }

    def parse_para(self, typ):
        """[summary]

        Args:
            typ ([str]): [数据库类型]
        """
        # key 为最终的key，value为配置文件中的值
        dbmap = {
            "postgresql" : {
                "host": "host",
                "port": "port",
                "database": "dbname",
                "user": "user",
                "password": "password",
                "min_size": "minconn",
                "max_size": "maxconn"
            },
            "mysql" : {
                "host" : "host",
                "port" : "port",
                "user" : "user",
                "password" : "password",
                "db" : "dbname",
                "charset" : "charset",
                "maxsize" : "maxconn",
                "minsize" : "minconn",
  
            },
            "mongo" : {
                "url" : "url", 
                "collection": "collection"
            }
        }
        return dbmap[typ]

    def read_db(self, typ:str):
        """
        default: PostgreSQL
        """
        dbname = self.check_db_type("db-"+typ)
        assert dbname is not None, "不支持所选数据库: [{0}]".format(dbname)
        dbfields = self.parse_para(typ)
        res = {}
        for name, value in dbfields.items():
            res.update({
                name: self.config.get(dbname).get(value)
            })
        return res

    def read_redis(self):
        return {
            "host": self.config.get("redis").get("host", None),
            "port": self.config.get("redis").get("port", None),
            "db": self.config.get("redis").get("db", None),
            "password": self.config.get("redis").get("password", None)
        }