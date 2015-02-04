from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
#migrate
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mobility.decorators import mobile_template
from flask.ext.mobility import Mobility
from flask.ext.script import Manager

from flask_oauth import OAuth

from Crypto.Cipher import AES

from config import config_update

# Create Flask Application Instance
app = Flask('application')

# Update config
config_update(app)


Mobility(app)
# Import application configuration file


db = SQLAlchemy(app)

manager = Manager(app)
migrate= Migrate(app,db)
manager.add_command('db', MigrateCommand)



oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FACEBOOK_APP_ID'],
    consumer_secret=app.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': ('email, ')}
)


aes = AES.new(app.config['SECRET_KEY'])



from application.models import schema

# Import Every function in 'controllers' directory
for base, dirs, names in os.walk(os.path.join('application', 'controllers')):
    for name in filter(lambda s: s.endswith('.py') and s != '__init__.py', names) :
        exec('from application.controllers.'+name[:-3]+' import *')


# Import Every function in 'rest' directory
for base, dirs, names in os.walk(os.path.join('application', 'rest')):
    for name in filter(lambda s: s.endswith('.py') and s != '__init__.py', names) :
        exec('from application.rest.'+name[:-3]+' import *')

