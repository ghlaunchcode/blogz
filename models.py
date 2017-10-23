"""Models (Tables) for BLOGz"""
#models.py
# BLOGz-specific Models
#
# To init database tables, run this file with python:
# `python models.py`
#
# 2017, Geoffrey Hadler [for LC101:u2]

from datetime import datetime
from app import db, bcrypt
#, BlogzUser, BlogzEntry
#from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
#from flask_bcrypt import generate_password_hash

#db = SQLAlchemy()

# BLOGz User Model
class BlogzUser(db.Model):
    """Provide BlogzUser Model"""
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(127), unique=True)
    pass_hash = db.Column(db.String(60))
    email = db.Column(db.String(255), unique=True)
    level = db.Column(db.Integer)
    posts = db.relationship("BlogzEntry", backref="owner")
    #workaround for posts enumeration
    @hybrid_property
    def count(self):
        return len(self.posts)

    def __init__(self, handle, password, email, level):
        self.handle = handle
        self.pass_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.email = email
        self.level = level
        #self.count = 0

# BLOGz Entry Model
class BlogzEntry(db.Model):
    """Provide BlogzEntry Model"""
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('blogz_user.id'))
    title = db.Column(db.String(255))
    entry = db.Column(db.Text)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    edit_count = db.Column(db.Integer)
    #workaround for owner handle
    @hybrid_property
    def user(self):
        return BlogzUser.query.filter_by(id=self.owner_id).first().handle

    def __init__(self, owner, title, entry):
        #self.user = user
        self.owner = owner
        self.title = title
        self.entry = entry
        #Stored as UTC, will render in SERVER local zone
        self.created = self.modified = datetime.utcnow()
        self.edit_count = 0

# Create the tables and a default user
def initDB():
    print("BLOGz MODELS :: INIT")
    print("  + CREATE TABLES")
    db.create_all()
    print("  + CREATE USER root")
    print("\thandle: root\n\tpass: root\n\temail: root@localhost\n\tlevel: 7")
    new_user = BlogzUser("root", "root", "root@localhost", 7)
    new_user = BlogzUser("root", "root", "root@localhost", 7)
    #new_user.count = 1
    db.session.add(new_user)
    #print("  + COMMIT")
    #db.session.commit()
    print("  + CREATE ENTRY welcome")
    new_entry = BlogzEntry(new_user, "Welcome", "First!\nAnyways, welcome to 'the BLOGz'!")
    db.session.add(new_entry)
    print("  + COMMIT")
    db.session.commit()
    print("OK!")

if __name__ == "__main__":
    initDB()
