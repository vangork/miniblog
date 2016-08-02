python miniblog
===============

This is a simple blog implemented by Python. All is based on OSS technology.
Installs and configures Python.  Manage python packages with `pip` and `virtualenv` isolated Python environments.

####### THIS PROJECT IS TO DEMO HOW AZURE ENABLES OSS

You can go to [demooss.azurewebsites.net](http://demooss.azurewebsites.net/) to check how the website looks. 
Hope this can give you a basic idea how to leverage Azure to speed up your business togheter with OSS technology.

Development Environment Setup
------------
### Platforms

All the following steps apply to a clean Ubuntu Server 14.04.4 LTS. You can bypass some of the steps according to your own environment
or change the commmands accrodingly for the other Linux distributions.

### Steps

1.Install git and clone this project from the github repository

```bash
# install git
$ sudo apt-get install git

# clone the code and switch the project folder
$ git clone xxxxxxxxx
$ cd miniblog
```

2.By default, Python3.4.3 has been intergraded with Ubuntu Server 14.04.4 LTS.
But we need to install `pip` and `virtualenv` with the following command.

```bash
# install pip
$ sudo apt-get install python3-pip

# Once pip is installed, you can use it to install the virtualenv package.
$ sudo pip3 install virtualenv
```
3.Now, create a virtual environment within the project directory by typing:
```bash
$ virtualenv env 
```
This will install a standalone version of Python, as well as `pip` and `wheel`, 
into an isolated directory structure within your project directory. 
We chose to call our virtual environment `env`, but you can name it something descriptive. 
A directory will be created with the name you select, 
which will hold the file hierarchy where your packages will be installed.

4.To install packages into the isolated environment, you must activate it by typing:
```bash
$ source env/bin/activate
```

5.Now we could proceed to install the requried packages for this project defined in requirements.txt
```bash
$ pip install -r requirements.txt
```

6.Customize the parameter in the config.py accordingly.

#####Database   
By default, this application will use SQLite DB named miniblog.db located in the root path as the backend database.
Make sure to create a empty one if it dosen't exist.  
```
$ touch miniblog.db 
```
To use MySQL Database, change the following value. In additional, 
create the database with the name of value of MYSQL_DATABASE in the MySQL instance.
```
DATABASR_TYPE = 'mysql'  # Change DATABASR_TYPE to 'mysql' 
MYSQL_SERVER = 'server'   
MYSQL_DATABASE = 'miniblog'
MYSQL_USER = 'user'   
MYSQL_PASSWORD = 'password'   
```
To use Microsoft SQL Server Database, change the following value. In additional, 
create the Database with the name of value of MSSQL_DATABASE in the SQL Server instance.
```
DATABASR_TYPE = 'mssql'   # Change DATABASR_TYPE to 'mssql'
MSSQL_SERVER = 'server'
MSSQL_DATABASE = 'miniblog'
MSSQL_USER = 'user'
MSSQL_PASSWORD = 'password' 
```
NOTE: It also supports `Postgres` and `Oracle`. You can rewrite `SQLALCHEMY_DATABASE_URI` value according to
[flask-sqlalchemy Connection URI Format](http://flask-sqlalchemy.pocoo.org/2.1/config/#connection-uri-format)
if needed.

#####Session   
By default, this application will use client-side sessions  
To use redis, change the following value:
```
SESSION_CLIENT = False #True(client-side session), False(server-side session)
REDIS_HOST = 'host'
REDIS_PORT = port
REDIS_PASSWORD = 'password'
```
NOTE: It also supports `memcached`, `filesystem`, `mongodb` and `sqlalchemy`. You can rewrite `SESSION_TYPE` value 
and add some other environemnt parameters according to [flask-session ](https://pythonhosted.org/Flask-Session/)
if needed.   

#####Mail Server & ServiceBus Queue  
This part is to support the functionality of automatic email nofication to administrators when error 500 is hit.
And password forgotten reset link will also be sent by the same email account.
Please set the sender mailbox smtp info, and receiver list.
```
## Mail Config
MAIL_SERVER = 'sender mailbox smtp-server'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'sender mailbox user'
MAIL_PASSWORD = 'sender mailbox password'
MAIL_RECEIVER = 'receiver email addresses'
## Service Bus Config
AZURE_SERVICE_BUS_SERVICE_NAMESPACE = 'bus name'
AZURE_SERVICE_BUS_QUEUE = 'queue'
AZURE_SERVICE_BUS_SHARED_ACCESS_KEY_NAME = 'access key name'
AZURE_SERVICE_BUS_SHARED_ACCESS_KEY_VALUE = 'access key value'
```
#####CDN
Provide with the CDN info so as to improve the performance by pointing the static url to CDN. By default, it is disabled.
```
CDN_ENABLED = False # True to enable CDN, False to disable
CDN_DOMAIN = 'domain name'
```

7.Initialize the database schema and run the program
```
# Initialize DB schema
$ python db_create.py

# Start the application 
$ python runserver.py
```
Now you will see the following output in the console and 
it is the TIME to open your web browser and navigate to http://localhost:5555/.
```
 * Running on http://localhost:5555/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: xxx-xxx-xxx
```

Deploy To Production
----------

##### 1. Go to [New Azure portal](http://portal.azure.com), and create the following Azure Services.   
* Web App
* SQL Datebase
* Redis Cache
* CDN Profile
* Service Bus

##### 2. Change the config based on the step 6 in the last chapter.

##### 3. Follow the link below to enable the web app repository and deploy the project  
https://azure.microsoft.com/en-us/documentation/articles/web-sites-publish-source-control/

License & Authors
-----------------
- Author: Yi Liu (<lyi@microsoft.com>)
- License: GNU GENERAL PUBLIC LICENSE

