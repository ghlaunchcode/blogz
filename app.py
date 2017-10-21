#! /usr/bin/python3

# app.py
# Build A Blog
# 2017, polarysekt

# imports
from flask import Flask, Markup, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt


import time
from datetime import datetime
import pytz
from tzlocal import get_localzone

import os

#from models import db, BlogzUser, BlogzEntry
from gh_slogan import getSlogan

## ENABLE/DISABLE Debugging ###
ghDEBUG = True
###############################

app = Flask( __name__ )
app.config['DEBUG'] = ghDEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO' ] = False #ghDEBUG

#for late-loading (comes from models.py)
#db.init_app(app)
db = SQLAlchemy( app )
bcrypt = Bcrypt( app )
asdl
app.secret_key = bcrypt.generate_password_hash( "mediumWicked" )

# BLOGz User Model
class BlogzUser( db.Model ):
    id = db.Column( db.Integer, primary_key = True )
    handle = db.Column( db.String( 127 ), unique = True )
    pass_hash = db.Column( db.String( 60 ) )
    email = db.Column( db.String( 255 ), unique = True )
    level = db.Column( db.Integer )
    posts = db.relationship("BlogzEntry", backref="owner")
    #workaround for posts enumeration
    @hybrid_property
    def count(self):
        return len(self.posts)
    
    def __init__( self, handle, password, email, level ):
        self.handle = handle
        self.pass_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.email = email
        self.level = level
        #self.count = 0

# BLOGz Entry Model
class BlogzEntry( db.Model ):
    id = db.Column( db.Integer, primary_key = True )
    #TODO reference user by id
    owner_id = db.Column( db.Integer, db.ForeignKey('blogz_user.id') )
    #user = db.Column( db.String(127) )
    title = db.Column( db.String( 255 ) )
    entry = db.Column( db.Text )
    created = db.Column( db.DateTime )
    modified = db.Column( db.DateTime )
    edit_count = db.Column( db.Integer )
    #workaround for owner handle
    @hybrid_property
    def user(self):
        return BlogzUser.query.filter_by( id = self.owner_id ).first().handle
    
    def __init__( self, owner, title, entry ):
        #self.user = user
        self.owner = owner
        self.title = title
        self.entry = entry
        #Stored as UTC, will render in SERVER local zone
        self.created = self.modified = datetime.utcnow()
        self.edit_count = 0


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

# Fun, but impractical
def gh_getFetchInfo():
    #utcTime = datetime.utcnow()
    #return "UTC: " + str(utcTime) + "<br/>" + time.strftime("%Z") + ": " + str(gh_getLocalTime(utcTime))    
    return ""

# Build user panel
def get_userdetails():
    userdetails = []
    if 'loglevel' in session:
        userdetails.append( session['handle'] )
        userdetails.append( '[<a href="logout">log out</a>]' )
    else:
        userdetails.append( request.remote_addr )
        userdetails.append( '[<a href="login">login</a> | <a href="signup">signup</a>]' )
    
    return userdetails

# Concise BLACKLIST / REDUNDANCY checking
@app.before_request
def verify_user():
    #TODO allow users to have privilege level :: currently just checks for >0
    
    #it's easier to do this here and now
    isAuthentic = False
    if 'loglevel' in session:
        if session['loglevel'] > 0:
            isAuthentic = True
    
    # Check for restricted pages
    if not isAuthentic:
        #CREATE blacklist (ONLY IF NECESSARY)
        restricted_routes = ['newpost', 'logout']
        if request.endpoint in restricted_routes:
            return redirect( "login", 302 )
    else:
        # Check for redundancy (logged users trying to relog or create)
        redundant_routes = ['login', 'signup']
        if request.endpoint in redundant_routes:
            return redirect( "/", 302 )


# ROUTE: '/' :: Main Site Index
# open access
@app.route( "/" )
def index( ):
    strNav = '<a href="/">' + ghSITE_NAME + '</a>'

    strErratae = gh_getFetchInfo()
    
    userdetails = get_userdetails()
    strSiteUserName = userdetails[0]
    strSiteUserMenu = userdetails[1]
    
    
    #get user list without pass_hash
    view_users = BlogzUser.query.options(load_only("handle","email", "level"))
    
    #for i in view_users:
    #    i.count = len(i.posts)
    #    print( i.handle, "=", i.count )
    
    return render_template('index.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_HOME, ghSlogan=getSlogan(), ghUser_Name=strSiteUserName, ghUser_Menu=Markup(strSiteUserMenu),ghNav=Markup(strNav), ghErratae=Markup(strErratae), ghUsers=view_users)

# ROUTE: '/features' :: Feature List Page

# ROUTE: '/blog' :: Blog View Page
# open access
@app.route( "/blog" )
def blog( ):
    #TODO adjust nav string if different view (single, user)    
    strNav = '<a href="/">' + ghSITE_NAME + '</a>' + " :: " + '<a href="/blog">' + ghPAGE_BLOG + '</a>'
    strErratae = gh_getFetchInfo()
    userdetails = get_userdetails()
    strSiteUserName = userdetails[0]
    strSiteUserMenu = userdetails[1]

    # DETERMINE view TYPE
    strUserName = request.args.get('user')
    strViewId = request.args.get('id')
    if strViewId == None:
        intViewId = 0
    else:
        try:
            intViewId = int(strViewId)
        except:
            intViewId = 0
        
    #print( strUserName )
    if strUserName == None:
        if intViewId > 0:
            strNav += ' :: <a href="?id=' + strViewId + '">id=' + strViewId + '</a>'
            view_entries = BlogzEntry.query.filter_by(id=intViewId)
        else:
            strNav += ' :: <a href="blog">all</a>'
            view_entries = BlogzEntry.query.all()
    else:
        #Get owner_id
        #TODO load_only?
        intOwnerId = BlogzUser.query.filter_by(handle=strUserName).first().id
        strNav += ' :: <a href="?user=' + strUserName + '">' + strUserName + "</a>"
        if intViewId > 0:
            strNav += ' & <a href="?id=' + strViewId + '">id=' + strViewId + '</a>'
            view_entries = BlogzEntry.query.filter_by( owner_id=intOwnerId, id=intViewId )
        else:
            view_entries = BlogzEntry.query.filter_by( owner_id=intOwnerId )
        
 
    #convert the dates to local server time
    #TODO get users local time?
    #if( len(view_entries) > 0 ):
    #TODO get the (user) field to persist
    for i in view_entries:
        i.created = gh_getLocalTime(i.created)
        
        
    #TODO if no view entries then dont send ghEntries
 
    return render_template('blog.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_BLOG, ghSlogan=getSlogan(), ghUser_Name=strSiteUserName, ghUser_Menu=Markup(strSiteUserMenu), ghNav=Markup(strNav), ghErratae=Markup(strErratae), ghEntries = view_entries)

# ROUTE '/login' :: User Login Page
# blacklist = redundancy
@app.route( "/login", methods=['POST', 'GET'] )
def login( ):
    strErrMsg = ""
    strUserName = ""
    
    strNav = '<a href="/">' + ghSITE_NAME + '</a>' + " :: " + '<a href="/login">' + ghPAGE_LOGIN + '</a>' 
    #TODO get from session if possible
    userdetails = get_userdetails()
    strSiteUserName = userdetails[0]
    strSiteUserMenu = userdetails[1]
    strErratae = gh_getFetchInfo()
    
    if request.method == 'POST':
        
        strUserName = request.form['inUserName']
        strUserPass = request.form['inUserPass']
        
        #TODO INPUT VALIDATION
        
        #if ghDEBUG:
            #print( "QUERY User Table..." )

        rowUserEntry = BlogzUser.query.filter_by( handle = strUserName ).first()

        #TODO: CHECK IF FOUND
        if rowUserEntry:
            isValidUser = True
        else:
            isValidUser = False
        
        #if ghDEBUG:
            #print( "Valid User:", isValidUser )

        if isValidUser:
            #if ghDEBUG:
                #print( rowUserEntry )
                #print( "handle:",rowUserEntry.handle,"pass:",rowUserEntry.pass_hash,"email:",rowUserEntry.email,"level:",rowUserEntry.level )
                #print( "Compare password hashes..." )
            
            isValidPassword = bcrypt.check_password_hash( rowUserEntry.pass_hash, strUserPass )
            
            #if ghDEBUG:
                #print( "isValidPassword:", isValidPassword )
                
            if isValidPassword:
                # LOG IN
                session['loglevel'] = rowUserEntry.level
                session['handle'] = rowUserEntry.handle
                return redirect("/blog?user="+session['handle'], 302)
            else:
                #TODO invalid password message??
                strErrMsg = "Invalid Password Specified"
        else:
            #TODO invalid user message??
            strErrMsg = "Invalid User Specified"
        
    return render_template('login.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_LOGIN, ghSlogan=getSlogan(), ghUser_Name=strSiteUserName, ghUser_Menu=Markup(strSiteUserMenu), ghNav=Markup(strNav), vErrMsg=strErrMsg, vUserName=strUserName, ghErratae=Markup(strErratae) )

# ROUTE '/logout' :: User Logout / End Session
# blacklist = restricted
@app.route( "/logout" )
def logout( ):
    #TODO interrim logout screen
    del session['handle']
    del session['loglevel']
    return redirect( "/", 302 )

#TODO
#def validate_signup( strUserName, strUserPass0, strUserPass1, strUserEmail):
    #return True

# ROUTE 'signup' :: User Signup -- separates POST / GET logic
# blacklist = redundant
@app.route( "/signup", methods=['POST','GET'] )
def signup( ):   
    # BUILD nav string
    strNav = '<a href="/">' + ghSITE_NAME + '</a>' + " :: " + '<a href="/signup">' + ghPAGE_SIGNUP + '</a>'
    userdetails = get_userdetails()
    strSiteUserName = userdetails[0]
    strSiteUserMenu = userdetails[1]
    strErratae = gh_getFetchInfo()
    
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
        ERRSTR_LENGTH_EMAIL = " Field must be 3 to 127 characters!"
        ERRSTR_USER_EXIST = " User already exists!"

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
        
        
        if len(strUserName) < 3 or len(strUserName) > 20:
            isSuccess = False
            statusUserName = ERRSTR_STATUS_ERROR
            strerrUserName += ERRSTR_LENGTH_FIELD

        # CHECK for SPACES
        # returns -1 if not found, else index
        if strUserName.find(" ") > -1:
            isSuccess = False
            statusUserName = ERRSTR_STATUS_ERROR
            strerrUserName += ERRSTR_SPACES_FIELD
            
        if len(strUserPass0) < 3 or len(strUserPass0) > 20:
            isSuccess = False
            statusUserPass0 = ERRSTR_STATUS_ERROR
            strerrUserPass0 += ERRSTR_LENGTH_FIELD
    
        if len(strUserPass1) < 3 or len(strUserPass1) > 20:
            isSuccess = False
            statusUserPass1 = ERRSTR_STATUS_ERROR
            strerrUserPass1 += ERRSTR_LENGTH_FIELD

        if strUserPass0 != strUserPass1:
            isSuccess = False
            statusUserPass0 = ERRSTR_STATUS_ERROR
            statusUserPass1 = ERRSTR_STATUS_ERROR
            strerrUserPass0 += ERRSTR_LENGTH_FIELD
            strerrUserPass1 += ERRSTR_LENGTH_FIELD

        # Only parse if email provided
        if strUserEmail != None:
            # CHECK for SPACES
            # returns -1 if not found, else index
            if strUserEmail.find(" ") > -1:
                isSuccess = False
                statusUserEmail = ERRSTR_STATUS_ERROR
                strerrUserEmail += ERRSTR_SPACES_FIELD
            # Look for @ (ignore period)
            if strUserEmail.find("@") == -1:
                isSuccess = False
                statusUserEmail = ERRSTR_STATUS_ERROR
                strerrUserEmail += ERRSTR_INVALID_EMAIL
            # Check length (higher bound for email)
            if len(strUserEmail) < 3 or len(strUserEmail) > 127:
                isSuccess = False
                statusUserEmail = ERRSTR_STATUS_ERROR
                strerrUserEmail += ERRSTR_LENGTH_EMAIL
        
        # only call db req if all else is good
        if isSuccess:
            user_hand = BlogzUser.query.filter_by( handle = strUserName ).options( load_only("handle") ).first()
            #if ghDEBUG:
                #print( user_hand )
                #print( user_hand.handle )
                #print( user_hand.id )
            if user_hand != None:
                isSuccess = False
                statusUserName = ERRSTR_STATUS_ERROR
                strerrUserName += ERRSTR_USER_EXIST
        
        if not isSuccess:
            return render_template('signup.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_SIGNUP, ghSlogan=getSlogan(), ghUser_Name=strSiteUserName, ghUser_Menu=Markup(strSiteUserMenu), ghNav=Markup(strNav), strUserName=strUserName, strUserEmail=strUserEmail, statusUserName=statusUserName, statusUserPass0=statusUserPass0, statusUserPass1=statusUserPass1, statusUserEmail=statusUserEmail, strerrUserName=strerrUserName, strerrUserPass0=strerrUserPass0, strerrUserPass1=strerrUserPass1, strerrUserEmail=strerrUserEmail, ghErratae=Markup(strErratae) )
        
        # fallthrough to commit new entry
        # default level is 1 / count is 0 behind scenes
        new_user = BlogzUser( strUserName, strUserPass0, strUserEmail, 1 )
        db.session.add(new_user)
        db.session.commit()
        # TODO redirect to an interrim info page?
        return redirect('login', 302)
    
    return render_template('signup.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_SIGNUP, ghSlogan=getSlogan(), ghUser_Name=strSiteUserName, ghUser_Menu=Markup(strSiteUserMenu), ghNav=Markup(strNav), ghErratae=Markup(strErratae) )

# ROUTE "/newpost" :: Create a new blog entry
# blacklist = restricted
@app.route( "/newpost", methods=['POST', 'GET'] )
def newpost( ):
    strNav = '<a href="/">' + ghSITE_NAME + '</a>' + " :: " + '<a href="/blog">' + ghPAGE_NEWPOST + '</a>'
    userdetails = get_userdetails()
    strSiteUserName = userdetails[0]
    strSiteUserMenu = userdetails[1]
    strErratae = gh_getFetchInfo()

    #TODO verify reqs
    if request.method == 'POST':
        isSuccess = True
        strerrTitle = ""
        strerrEntry = ""
        statusTitle = ""
        statusEntry = ""
        strTitle = request.form['inTitle']
        strEntry = request.form['inEntry']
        if( strTitle == "" ):
            isSuccess = False
            strerrTitle = "Post must contain a title"
        
        if( strEntry == "" ):
            strerrEntry = "Post must contain an entry"
            isSuccess = False
            
        if not isSuccess:
            return render_template('newpost.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_NEWPOST, ghSlogan=getSlogan(), ghUser_Name=strSiteUserName, ghUser_Menu=Markup(strSiteUserMenu), ghNav=Markup(strNav), ghErratae=Markup(strErratae), vTitle=strTitle, vEntry=strEntry, strerrTitle=strerrTitle, strerrEntry=strerrEntry )
        
        #if success
        owner = BlogzUser.query.filter_by(handle=session['handle']).first()
        new_post = BlogzEntry( owner, strTitle, strEntry )
#        owner.count = owner.count + 1
        db.session.add( new_post )
        db.session.commit()

        #TODO update owner with new post

        return redirect('blog?id='+str(new_post.id), 302)
    
    return render_template('newpost.html', ghSite_Name=ghSITE_NAME, ghPage_Title=ghPAGE_NEWPOST, ghSlogan=getSlogan(), ghUser_Name=strSiteUserName, ghUser_Menu=Markup(strSiteUserMenu), ghNav=Markup(strNav), ghErratae=Markup(strErratae) )

def main():
    app.run()

if __name__ == "__main__":
    main()
