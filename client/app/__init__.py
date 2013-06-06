import os
from flask import Flask
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')

from app import views
