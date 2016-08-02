from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from flask_cdn import CDN
from azure.servicebus import ServiceBusService
from config import AZURE_SERVICE_BUS_SERVICE_NAMESPACE, AZURE_SERVICE_BUS_SHARED_ACCESS_KEY_NAME, AZURE_SERVICE_BUS_SHARED_ACCESS_KEY_VALUE, SESSION_CLIENT, CDN_ENABLED

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = u'Please log in to access this page.'
lm.login_message_category = 'danger'
if not SESSION_CLIENT: 
    Session(app)
if CDN_ENABLED:
    CDN(app)

bus_service = ServiceBusService(service_namespace = AZURE_SERVICE_BUS_SERVICE_NAMESPACE, 
        shared_access_key_name = AZURE_SERVICE_BUS_SHARED_ACCESS_KEY_NAME, 
        shared_access_key_value = AZURE_SERVICE_BUS_SHARED_ACCESS_KEY_VALUE)





from miniblog import views
