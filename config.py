# Author: Alex Culp                              
# Description: config.py --  database and app configuration         

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

MAX_USERNAME = 64
MAX_CONTACT_INFO = 128
MAX_BIO = 512
MAX_SUMMARY = 1024

# web app and database configuration
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alex:meow@localhost/postgres'
db = SQLAlchemy(app)
