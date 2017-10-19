#! /usr/bin/python3

# app.py
# Build A Blog
# 2017, polarysekt

# imports
from flask import Flask, Markup, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

#TODO force utc and timezone offset awareness
import time
from datetime import datetime
#TimeZone and DST
import pytz
from tzlocal import get_localzone


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

ghDEBUG = True

ghSITE_NAME = "BLOGz"
ghPAGE_HOME = "home"
ghPAGE_BLOG = "posts"
ghPAGE_LOGIN = "login"
ghPAGE_SIGNUP = "signup"
ghPAGE_NEWPOST = "new post"

# some utils
def gh_getLocalTime( utc_dt ):
    loc_z = get_localzone()
    loc_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(loc_z)
    return loc_z.normalize(loc_dt)

#TODO
@app.before_request
def verify_user():
    ##TODO
    #if ghDEBUG:
        #req_utc = datetime.utcnow()
        #req_loc = gh_getLocalTime( req_utc )
        #print( "REQUEST @ ", req_utc, " => local:", req_loc, time.strftime("%Z") )
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
    strNav = '<a href="/">' + ghSITE_NAME + '</a>'
    utcTime = datetime.utcnow()
    strErratae = "Fetched @ " + str(utcTime) + " / " + str(gh_getLocalTime(utcTime))
    
    #get user list
    view_users = BlogzUser.query.all()
    #TODO return user name AND email
    #view_users = []
    #for i in users_data:
        #view_users.append( i.handle )

    # simple implementation (remove pass_hash)
    for i in view_users:
        i.pass_hash = ""

        
    if ghDEBUG:
        print( view_users )
    
    return render_template('index.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_HOME, ghSlogan=getSlogan(), ghUser_Name=request.remote_addr, ghNav=Markup(strNav), ghErratae=strErratae, ghUsers=view_users)

# ROUTE: '/features' :: Feature List Page

# ROUTE: '/blog' :: Blog View Page
@app.route( "/blog" )
def blog( ):
    strNav = '<a href="/">' + ghSITE_NAME + '</a>' + " :: " + '<a href="/blog">' + ghPAGE_BLOG + '</a>'
    #TODO adjust nav string if different view (single, user)
    return render_template('blog.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_BLOG, ghSlogan=getSlogan(), ghNav=Markup(strNav) )

@app.route( "/login", methods=['POST', 'GET'] )
def login( ):
    strErrMsg = ""
    strUserName = ""
    
    strNav = '<a href="/">' + ghSITE_NAME + '</a>' + " :: " + '<a href="/login">' + ghPAGE_LOGIN + '</a>' 
    
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
        
    return render_template('login.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_LOGIN, ghSlogan=getSlogan(), ghNav=Markup(strNav), vErrMsg=strErrMsg, vUserName=strUserName )

@app.route( "/logout" )
def logout( ):
    #TODO
    return redirect( "/", 302 )

def validate_signup( strUserName, strUserPass0, strUserPass1, strUserEmail):
    return True

# ROUTE 'signup' :: User Signup
# Now separates POST logic and variables
@app.route( "/signup", methods=['POST','GET'] )
def signup( ):   
    # BUILD nav string
    strNav = '<a href="/">' + ghSITE_NAME + '</a>' + " :: " + '<a href="/signup">' + ghPAGE_SIGNUP + '</a>'
    
    # POST condition
    if request.method == 'POST':
        #NOTE: error checking aggregates and falls through
        
        # Error Styling #TODO
        ERRSTR_STATUS_ERROR = "status-condition_ERROR"
        
        # Various ERROR messages
        ERRSTR_EMPTY_FIELD = " Field is required!"
        ERRSTR_LENGTH_FIELD = " Field must be 3 to 20 characters!"
        ERRSTR_SPACES_FIELD = " Field must not contain spaces!"
        ERRSTR_MATCH_FIELD = " Fields must match!"
        ERRSTR_INVALID_EMAIL = " Field must contain valid email!"

        # DECLARE / INIT form VARs
        strUserName = ""
        strUserPass0 = ""
        strUserPass1 = ""
        strUserEmail =""
        strerrUserName = ""
        strerrUserPass0 = ""
        strerrUserPass1 = ""
        strerrUserEmail = ""
        statusUserName = ""
        statusUserPass0 = ""
        statusUserPass1 = ""
        statusUserEmail = ""        
        
        # Obtain POSTed values
        strUserName = request.form['inUserName']
        strUserPass0 = request.form['inUserPass0']
        strUserPass1 = request.form['inUserPass1']
        strUserEmail = request.form['inUserEmail']
        
        # Set a success variable (optimistic)
        isSuccess = True
        
        
        # Begin VALIDATION
        # CHECK for EMPTY
        if strUserName == "":
            isSuccess = False
            statusUserName = ERRSTR_STATUS_ERROR
            strerrUserName += ERRSTR_EMPTY_FIELD
    
        if strUserPass0 == "":
            isSuccess = False
            statusUserPass0 = ERRSTR_STATUS_ERROR
            strerrUserPass0 += ERRSTR_EMPTY_FIELD
            
        if strUserPass1 == "":
            isSuccess = False
            statusUserPass1 = ERRSTR_STATUS_ERROR
            strerrUserPass1 += ERRSTR_EMPTY_FIELD
            
        #NOTE: email is not required
    
    
        return render_template('signup.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_SIGNUP, ghSlogan=getSlogan(), ghNav=Markup(strNav), strUserName=strUserName, strUserEmail=strUserEmail, statusUserName=statusUserName, statusUserPass0=statusUserPass0, statusUserPass1=statusUserPass1, statusUserEmail=statusUserEmail, strerrUserName=strerrUserName, strerrUserPass0=strerrUserPass0, strerrUserPass1=strerrUserPass1, strerrUserEmail=strerrUserEmail )
    
    return render_template('signup.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_SIGNUP, ghSlogan=getSlogan(), ghNav=Markup(strNav) )

@app.route( "/newpost", methods=['POST', 'GET'] )
def newpost( ):
    strNav = '<a href="/">' + ghSITE_NAME + '</a>' + " :: " + '<a href="/blog">' + ghPAGE_NEWPOST + '</a>'
    return render_template('newpost.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_NEWPOST, ghSlogan=getSlogan(), ghNav=Markup(strNav) )

def main():
    app.run()

if __name__ == "__main__":
    main()
