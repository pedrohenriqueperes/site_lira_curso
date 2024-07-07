from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)



app.config['SECRET_KEY'] = 'c70d27fa2912b9b0dda5cd10b19c0cc1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)

from comunidadeimpressionadora import routes