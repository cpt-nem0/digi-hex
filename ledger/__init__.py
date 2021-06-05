import os

from flask import Flask, app
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGODB_HOST'] = os.getenv('MONGO_URI') # remember to add DB here
app.config['MONGODB_CONNECT'] = False

try: 
    mongo = MongoEngine()
    mongo.init_app(app)
    print('Database connected!!')

except:
    print('Database connection failure')

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
message = MIMEMultipart()

from ledger import routes