from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e2a87a53bf8ea2b8cfd7fd1f80c70896'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/site.db'
app.config['MAX_STORAGE_TIME'] = 1440

db = SQLAlchemy(app)

from url_shortener import routes