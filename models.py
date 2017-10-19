#models.py
# BLOGz-specific Models
# TODO:
# To init database tables, run this file with python:
# `python models.py`
#
# 2017, Geoffrey Hadler [for LC101:u2]

#from app import db, BlogzUser, BlogzEntry
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash

db = SQLAlchemy()

# BLOGz User Model
class BlogzUser( db.Model ):
    id = db.Column( db.Integer, primary_key = True )
    handle = db.Column( db.String( 127 ) )
    pass_hash = db.Column( db.String( 60 ) )
    email = db.Column( db.String( 255 ) )
    level = db.Column( db.Integer )
    
    def __init__( self, handle, password, email, level ):
        self.handle = handle
        self.pass_hash = generate_password_hash(password).decode('utf-8')
        self.email = email
        self.level = level

# BLOGz Entry Model
class BlogzEntry( db.Model ):
    id = db.Column( db.Integer, primary_key = True )
    #TODO reference user by id
    #user = db.Column( db.Integer )
    user = db.Column( db.String(127) )
    title = db.Column( db.String( 255 ) )
    entry = db.Column( db.Text )
    created = db.Column( db.DateTime )
    modified = db.Column( db.DateTime )
    edit_count = db.Column( db.Integer )
    
    def __init__( self, user, title, entry ):
        self.user = user
        self.title = title
        self.entry = entry
        #Stored as UTC, will render in SERVER local zone
        self.created = self.modified = datetime.utcnow()
        self.edit_count = 0



# Create the tables and a default user
def initDB():
    print( "BLOGz MODELS :: INIT" )
    print( "  + CREATE TABLES" )
    db.create_all()
    print( "  + CREATE USER root" )
    print( "    handle: root\n    pass: root\n    email: root@localhost\n    level: 7" )
    new_user = BlogzUser( "root", "root", "root@localhost", 7 )
    db.session.add( new_user )
    print( "  + COMMIT" )
    db.session.commit()
    print( "  + CREATE ENTRY welcome" )
    new_entry = BlogzEntry( "root", "Welcome", "First!\nAnyways, welcome to 'the BLOGz'!" )
    db.session.add( new_entry )
    print( "  + COMMIT" )
    db.session.commit()
    print( "OK!" )

if __name__ == "__main__":
    initDB()
    
