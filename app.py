#! /usr/bin/python3

# app.py
# Build A Blog
# 2017, polarysekt

# imports
from flask import Flask, Markup, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from gh_slogan import getSlogan


app = Flask( __name__ )
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#g_app.config['SQLALCHEMY_ECHO' ] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class BlogzUser( db.Model ):
    id = db.Column( db.Integer, primary_key = True )
    handle = db.Column( db.String( 127 ) )
    pass_hash = db.Column( db.String( 60 ) )
    email = db.Column( db.String( 255 ) )
    level = db.Column( db.Integer )
    
    def __init__( self, handle, password, email, level ):
        self.handle = handle
        self.pass_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.email = email
        self.level = level


ghDEBUG = True

ghSITE_NAME = "BLOGz"
ghPAGE_HOME = "home"
ghPAGE_BLOG = "posts"


#TODO
@app.before_request
def verify_user():
    ##TODO
    #if ghDEBUG:
        #testHash = (bcrypt.generate_password_hash('test').decode('utf-8'))
        #print (testHash, len(testHash))
    #if session['logLevel'] > 0:
        #Allow User
    #else:
        #Redirect User
    #return redirect( "/", 302 )
    placeholder = 0

# ROUTE: '/' :: Main Site Index
@app.route( "/" )
def index( ):
    return render_template('index.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_HOME, ghSlogan=getSlogan(), ghUser_Name=request.remote_addr)

# ROUTE: '/blog' :: Blog View Page
@app.route( "/blog" )
def blog( ):
    return render_template('blog.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_BLOG, ghSlogan=getSlogan() )

@app.route( "/login", methods=['POST'] )
def login( ):
    strErrMsg = ""
    strUserName = ""
    if request.method == 'POST':
        
        strUserName = request.form['inUserName']
        strUserPass = request.form['inUserPass']
        
        #TODO INPUT VALIDATION
        
        if ghDEBUG:
            print( "QUERY User Table..." )

        rowUserEntry = BlogzUser.query.filter_by( handle = strUserName ).first()

        #TODO: CHECK IF FOUND
        if rowUserEntry:
            isValidUser = True
        else:
            isValidUser = False
        
        if ghDEBUG:
            print( "Valid User:", isValidUser )

        if isValidUser:
            if ghDEBUG:
                print( rowUserEntry )
                print( "handle:",rowUserEntry.handle,"pass:",rowUserEntry.pass_hash,"email:",rowUserEntry.email,"level:",rowUserEntry.level )
                
            if ghDEBUG:
                print( "Compare password hashes..." )
            
            isValidPassword = bcrypt.check_password_hash( rowUserEntry.pass_hash, strUserPass )
            
            if ghDEBUG:
                print( isValidPassword )
                
            if isValidPassword:
                #TODO login 
                placeholder = 0
            else:
                #TODO invalid password message??
                strErrMsg = "Invalid Password Specified"
        else:
            #TODO invalid user message??
            strErrMsg = "Invalid User Specified"
        
    return render_template('login.html', ghSite_Name=ghSITE_NAME, ghPage_Title="Login", ghSlogan=getSlogan(), vErrMsg=strErrMsg, vUserName=strUserName )

@app.route( "/logout" )
def logout( ):
    #TODO
    return redirect( "/", 302 )

@app.route( "/signup", methods=['POST'] )
def signup( ):
    if request.method == 'POST':
        strUserName = request.form['inUserName']
        strUserPass0 = request.form['inUserPass0']
        strUserPass1 = request.form['inUserPass1']
        strUserEmail = request.form['inUserEmail']
    return render_template('signup.html', ghSite_Name=ghSITE_NAME, ghPage_Title="User Signup", ghSlogan=getSlogan() )

@app.route( "/newpost" )
def newpost( ):
    return render_template('newpost.html', ghSite_Name=ghSITE_NAME, ghPage_Title="New Post", ghSlogan=getSlogan() )

def main():
    app.run()

if __name__ == "__main__":
    main()
