import redis
import os
import sys
import datetime
CSRF_ENABLED = True
SECRET_KEY = 'secret_key'
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSTS_PER_PAGE = 20

DATABASR_TYPE = 'sqlite'

MYSQL_SERVER = 'server'
MYSQL_DATABASE = 'miniblog'
MYSQL_USER = 'user'
MYSQL_PASSWORD = 'password'

MSSQL_SERVER = 'server'
MSSQL_DATABASE = 'miniblog'
MSSQL_USER = 'user'
MSSQL_PASSWORD = 'password'

if DATABASR_TYPE == 'mysql':
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_SERVER + '/' + MYSQL_DATABASE
elif DATABASR_TYPE == 'mssql':
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://' + MSSQL_USER + ':' + MSSQL_PASSWORD + '@' + MSSQL_SERVER + ':1433/' + MSSQL_DATABASE + '?charset=utf8&tds_version=7.0'
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.split(os.path.realpath(__file__))[0] + '\\miniblog.db'

SESSION_CLIENT = True
SESSION_TYPE = 'redis'
REDIS_HOST = 'host'
REDIS_PORT = 6380
REDIS_PASSWORD = 'password'
SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT, db=0, password=REDIS_PASSWORD, ssl=True)
PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=30)

MAIL_SERVER = 'server'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'xxx@outlook.com'
MAIL_PASSWORD = 'password'
MAIL_RECEIVER = 'xxx@live.com'

AZURE_SERVICE_BUS_SERVICE_NAMESPACE = 'namespace'
AZURE_SERVICE_BUS_QUEUE = 'queue'
AZURE_SERVICE_BUS_SHARED_ACCESS_KEY_NAME = 'RootManageSharedAccessKey'
AZURE_SERVICE_BUS_SHARED_ACCESS_KEY_VALUE = 'key_value'

CDN_ENABLED = False
CDN_DOMAIN = 'domain'