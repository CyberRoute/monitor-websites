
class Config:
    DEBUG = False
    TESTING = False
    PROCS = 8
    DOWN = 'UNREACHABLE'
    REFRESH = 60
    URLS = 'config/urls.json'
    SERVER_KAFKA = "kafka-host:18158"
    ssl_cafile = "ca.pem"
    ssl_certfile = "service.cert"
    ssl_keyfile = "service.key"
    #POSTGRES CONF
    DB_PASSWORD = "password"
    DB = "defaultdb"
    DBHOST = "pg-host"
    DBUSER = "avnadmin"
    DBTABLE = "monstats"


class ProductionConfig(Config):
    PROCS = 4
    DOWN = 'UNREACHABLE'
    REFRESH = 60


class DevelopmentConfig(Config):
    DEBUG = True
    PROCS = 4
    DOWN = 'UNREACHABLE'
    REFRESH = 60


class TestingConfig(Config):
    TESTING = True