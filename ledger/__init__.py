import os

from flask import Flask, app
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGODB_HOST'] = ''.join(os.getenv('MONGO_URI')+os.getenv('DB_NAME'))
app.config['MONGODB_CONNECT'] = False

mongo = MongoEngine()
mongo.init_app(app)

from ledger import routes