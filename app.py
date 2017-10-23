""" Provides app, db, and ghDEBUG """
# app.py
# Build A Blog
# 2017, polarysekt

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

## ENABLE/DISABLE Debugging ###
ghDEBUG = True
###############################

app = Flask(__name__)
app.config['DEBUG'] = ghDEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False #cghDEBUG

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.secret_key = bcrypt.generate_password_hash("mediumWicked").decode('utf-8')
valid_session_key = bcrypt.generate_password_hash("uservalid").decode('utf-8')
