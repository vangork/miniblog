import sys
import os
from email.mime.text import MIMEText
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from email_template import generate_mail_body
import json

#package_path = os.path.split(os.path.realpath(__file__))[0].replace('app_data\\jobs\\continuous\\QueueMonitor','env\\Lib\\site-packages')
config_path = os.path.split(os.path.realpath(__file__))[0][0:-len('\\app_data\\jobs\\continuous\\QueueMonitor')]
sys.path.append("d:\home\site\wwwroot\env\Lib\site-packages")
sys.path.append("d:\home\site\wwwroot")
sys.path.append(config_path)
from azure.servicebus import ServiceBusService, Message, Queue
from config import AZURE_SERVICE_BUS_SERVICE_NAMESPACE, AZURE_SERVICE_BUS_SHARED_ACCESS_KEY_NAME, AZURE_SERVICE_BUS_SHARED_ACCESS_KEY_VALUE, AZURE_SERVICE_BUS_QUEUE, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_RECEIVER

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

bus_service = ServiceBusService(service_namespace = AZURE_SERVICE_BUS_SERVICE_NAMESPACE, 
        shared_access_key_name = AZURE_SERVICE_BUS_SHARED_ACCESS_KEY_NAME, 
        shared_access_key_value = AZURE_SERVICE_BUS_SHARED_ACCESS_KEY_VALUE)
msg = bus_service.receive_queue_message(AZURE_SERVICE_BUS_QUEUE, peek_lock = False, timeout = 30)
if 'reset_email_type' in msg.custom_properties:
    from_addr = MAIL_USERNAME
    password = MAIL_PASSWORD
    properties = json.loads(msg.body.decode('utf-8'))
    to_addr = properties['reset_email']
    host = properties['reset_host']
    username = properties['reset_username']
    secret_key = properties['reset_secret_key']
    reset_link = 'http://' + host + '/reset/' + username + '/' + secret_key
    message = generate_mail_body(['Hello {0},'.format(username), '',
        'Please click the following link to reset your password within 30 mins.',
        '<a href={0}>{1}</a>'.format(reset_link, reset_link)
    ])
    msg = MIMEText(message, 'html', 'utf-8')
    msg['From'] = _format_addr('miniblog admin <%s>' % from_addr)
    msg['To'] = _format_addr('IT Admin <%s>' % to_addr)
    msg['Subject'] = Header('Password resert link from miniblog', 'utf-8').encode()

    server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
    if MAIL_USE_TLS == True:
        server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    print('reset mail sent')
elif 'alert_email_type' in msg.custom_properties:
    from_addr = MAIL_USERNAME
    password = MAIL_PASSWORD
    to_addr = MAIL_RECEIVER
    message = json.loads(msg.body.decode('utf-8'))
    message = generate_mail_body(['Hello Admin,', ''] + message)
    msg = MIMEText(message, 'html', 'utf-8')
    msg['From'] = _format_addr('miniblog alert <%s>' % from_addr)
    msg['To'] = _format_addr('IT Admin <%s>' % to_addr)
    msg['Subject'] = Header('error 500 was hit', 'utf-8').encode()

    server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
    if MAIL_USE_TLS == True:
        server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    print('alert mail sent')
else:
    print('no error')