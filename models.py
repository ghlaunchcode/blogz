#models.py
# BLOGz-specific Models
# TODO:
# To init database, run this file:
# `python models.py`
#
# 2017, Geoffrey Hadler [for LC101:u2]

from app import db, BlogzUser, BlogzEntry



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
    print( "OK!" )

if __name__ == "__main__":
    initDB()
    
