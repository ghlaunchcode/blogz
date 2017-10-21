""" Provides app, db, and ghDEBUG """
# app.py
# Build A Blog
# 2017, polarysekt

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

## ENABLE/DISABLE Debugging ###
ghDEBUG = False
isHeroku = True
###############################

app = Flask(__name__)
app.config['DEBUG'] = ghDEBUG

if isHeroku:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sotedygyjbbnwp:19eb3f2d2e21d3c02304912fc04b9dbe51144f5686f5a272a374f33db601b9d3@ec2-23-21-158-253.compute-1.amazonaws.com:5432/d392l7jnvv5tde'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'    

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False #cghDEBUG

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.secret_key = bcrypt.generate_password_hash( "mediumWicked" ).decode('utf-8')
valid_session_key = bcrypt.generate_password_hash( "uservalid" ).decode('utf-8')
