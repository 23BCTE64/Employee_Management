from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import db   
from model import Employee
from routes import main_blueprint
from config  import   Config
app = Flask(__name__)

app.config.from_object('config.Config')
db = SQLAlchemy(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
