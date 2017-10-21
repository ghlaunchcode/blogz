#! mega/bin/python

#models.py
# BLOGz-specific Models
# TODO:
# To init database tables, run this file with python:
# `python models.py`
#
# 2017, Geoffrey Hadler [for LC101:u2]

from app import db, BlogzUser, BlogzEntry
#from flask_sqlalchemy import SQLAlchemy
#from flask_bcrypt import generate_password_hash

#db = SQLAlchemy()


# Create the tables and a default user
def initDB():
    print( "BLOGz MODELS :: INIT" )
    print( "  + CREATE TABLES" )
    db.create_all()
    print( "  + CREATE USER root" )
    print( "    handle: root\n    pass: root\n    email: root@localhost\n    level: 7" )
    new_user = BlogzUser( "root", "root", "root@localhost", 7 )
    new_user = BlogzUser( "root", "root", "root@localhost", 7 )
    #new_user.count = 1
    db.session.add( new_user )
    print( "  + COMMIT" )
    db.session.commit()
    print( "  + CREATE ENTRY welcome" )
    new_entry = BlogzEntry( new_user, "Welcome", "First!\nAnyways, welcome to 'the BLOGz'!" )
    db.session.add( new_entry )
    print( "  + COMMIT" )
    db.session.commit()
    print( "OK!" )

if __name__ == "__main__":
    initDB()
    
