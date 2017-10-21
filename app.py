#! mega/bin/python

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
from gh_strings import *

## ENABLE/DISABLE Debugging ###
ghDEBUG = True
###############################

app = Flask( __name__ )
app.config['DEBUG'] = ghDEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False #ghDEBUG

#for late-loading (comes from models.py)
#db.init_app(app)
db = SQLAlchemy( app )
bcrypt = Bcrypt( app )

app.secret_key = bcrypt.generate_password_hash( "mediumWicked" ).decode('utf-8')

valid_session_key = bcrypt.generate_password_hash( "uservalid" ).decode('utf-8')

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

# some utils
def gh_getLocalTime( utc_dt ):
    loc_z = get_localzone()
    loc_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(loc_z)
    return loc_z.normalize(loc_dt)

def get_fetch_info():
    if ghDEBUG:
        utcTime = datetime.utcnow()
        return "UTC: " + str(utcTime) + "<br/>" + time.strftime("%Z") + ": " + str(gh_getLocalTime(utcTime))    
    else:
        return ""

def get_current_user():
    if valid_session_key in session:
        return session['handle']
    else:
        return request.remote_addr

def get_user_menu():
    if valid_session_key in session:
        return '[<a href="newpost">new post</a> | <a href="logout">log out</a>]'
    else:
        return '[<a href="login">log in</a> | <a href="signup">sign up</a>]'

# Concise BLACKLIST / REDUNDANCY checking
@app.before_request
def verify_user():
    #TODO allow users to have privilege level :: currently just checks for >0
    
    #it's easier to do this here and now
    isAuthentic = False
    if valid_session_key in session:
        if session['loglevel'] > 0:
            isAuthentic = True
    
    # Check for restricted pages
    if not isAuthentic:
        #CREATE blacklist (ONLY IF NECESSARY)
        restricted_routes = ['newpost', 'logout']
        if request.endpoint in restricted_routes:
            return redirect( "login?target="+request.endpoint, 302 )
    else:
        # Check for redundancy (logged users trying to relog or create)
        redundant_routes = ['login', 'signup']
        if request.endpoint in redundant_routes:
            return redirect( "/", 302 )

# ROUTE: '/' :: Main Site Index : open access
@app.route( "/" )
def index( ):
    return render_template('index.html',ghSite_Name=ghSITE_NAME,ghPage_Title=ghPAGE_HOME,ghSlogan=getSlogan(),ghUser_Name=get_current_user(), ghUser_Menu=Markup(get_user_menu()),ghNav=Markup(strNav_base),ghErratae=get_fetch_info(),ghUsers=BlogzUser.query.options(load_only("handle","email", "level")) )

# ROUTE: '/blog' :: Blog View Page : open access
@app.route( "/blog" )
def blog( ):
    strNav = strNav_base + " :: " + '<a href="/blog">' + ghPAGE_BLOG + '</a>'

    # DETERMINE view TYPE
    strUserName = request.args.get('user')
    strViewId = request.args.get('id')

    if strViewId:
        try:
            intViewId = int(strViewId)
        except:
            intViewId = 0
    else:
        intViewId = 0
    
    if strUserName:
        #Get owner_id
        #TODO load_only?
        intOwnerId = BlogzUser.query.filter_by(handle=strUserName).first().id
        strNav += ' :: <a href="?user=' + strUserName + '">' + strUserName + "</a>"
        if intViewId > 0:
            strNav += ' & <a href="?id=' + strViewId + '">id=' + strViewId + '</a>'
            view_entries = BlogzEntry.query.filter_by( owner_id=intOwnerId, id=intViewId )
        else:
            view_entries = BlogzEntry.query.filter_by( owner_id=intOwnerId )
    else:
        if intViewId > 0:
            strNav += ' :: <a href="?id=' + strViewId + '">id=' + strViewId + '</a>'
            view_entries = BlogzEntry.query.filter_by(id=intViewId)
        else:
            strNav += ' :: <a href="blog">all</a>'
            view_entries = BlogzEntry.query.all()
 
    #convert the dates to local server time
    #TODO get users local time?
    for i in view_entries:
        i.created = gh_getLocalTime(i.created)
         
    return render_template('blog.html',ghSite_Name=ghSITE_NAME,ghPage_Title=ghPAGE_BLOG,ghSlogan=getSlogan(),ghUser_Name=get_current_user(),ghUser_Menu=Markup(get_user_menu()),ghNav=Markup(strNav),ghErratae=get_fetch_info(),ghEntries=view_entries)

# ROUTE '/login' :: User Login Page : Redundancy Blacklist
@app.route( "/login", methods=['POST', 'GET'] )
def login( ):
    strNav = strNav_base + " :: " + '<a href="/login">' + ghPAGE_LOGIN + '</a>' 

    strUserName = ""
    strUserPass = ""

    strerrUserName = ""
    strerrUserPass = ""
    ssUserName = ""
    ssUserPass = ""

    if request.method == 'POST':

        strUserName = request.form['inUserName']
        strUserPass = request.form['inUserPass']
        
        # CHECK if BLANK User Name
        if strUserName:
            # CHECK if BLANK Password
            if strUserPass:
                # CHECK if FOUND
                rowUserEntry = BlogzUser.query.filter_by( handle = strUserName ).first()
                if rowUserEntry:
                    # CHECK PASSWORD
                    if bcrypt.check_password_hash( rowUserEntry.pass_hash, strUserPass ):

                        # LOG IN
                        #TODO: set the valid key to something random
                        session[valid_session_key] = "legit"
                        session['loglevel'] = rowUserEntry.level
                        session['handle'] = rowUserEntry.handle
                    
                        ##strTarget = request.args.get['target']
                        #if not target:
                            #return redirect("/"+target, 302)
                        #else:
                        return redirect("/blog?user="+session['handle'], 302)
                    
                    else:
                        #FAILED PASS CHECK
                        ssUserPass = ERRSTR_STATUS_ERROR
                        strerrUserPass = ERRSTR_BAD_PASS
                else:
                    # FAILED USER CHECK
                    ssUserName = ERRSTR_STATUS_ERROR
                    strerrUserName = ERRSTR_USER_NOT_FOUND
            else:
                # FAILED BLANK PASS CHECK
                ssUserPass = ERRSTR_STATUS_ERROR
                strerrUserPass = ERRSTR_EMPTY_FIELD
        else:
            # FAILED BLANK USER CHECK
            ssUserName = ERRSTR_STATUS_ERROR
            strerrUserName = ERRSTR_EMPTY_FIELD

            # CHECK PASSWORD (for full error report)
            if not strUserPass:
                ssUserPass = ERRSTR_STATUS_ERROR
                strerrUserPass = ERRSTR_EMPTY_FIELD
        
    return render_template('login.html',ghSite_Name=ghSITE_NAME,ghPage_Title=ghPAGE_LOGIN,ghSlogan=getSlogan(),ghUser_Name=get_current_user(),ghUser_Menu=Markup(get_user_menu()),ghNav=Markup(strNav),vUserName=strUserName,statusUserName=ssUserName,strerrUserName=strerrUserName,statusUserPass=ssUserPass,strerrUserPass=strerrUserPass,ghErratae=get_fetch_info() )

# ROUTE '/logout' :: User Logout / End Session : Restricted Blacklist
@app.route( "/logout" )
def logout( ):
    del session[ valid_session_key ]
    return redirect( "/", 302 )

class ValidateSignup:

    def __init__(self, strUserName, strUserPass0, strUserPass1, strUserEmail ):
        # For Form Data
        self.strUserName = strUserName
        self.strUserPass = [ strUserPass0, strUserPass1 ]
        self.strUserEmail = strUserEmail
        # For Errors
        self.errUserName = ""
        self.errUserPass = [ "", "" ]
        self.errUserEmail = ""
        # For Status Style
        self.ssUserName = ""
        self.ssUserPass = [ "", "" ]
        self.ssUserEmail = ""

    def isValid(self):
        # Begin VALIDATION
        isSuccess = True

        # CHECK for EMPTY
        if self.strUserName == "":
            isSuccess = False
            self.ssUserName = ERRSTR_STATUS_ERROR
            self.errUserName += ERRSTR_EMPTY_FIELD

        # CHECK for LENGTH
        if len(self.strUserName) < 3:
            isSuccess = False
            self.ssUserName = ERRSTR_STATUS_ERROR
            self.errUserName += ERRSTR_SHORT_FIELD_3

        if len(self.strUserName) > 20:
            isSuccess = False
            self.ssUserName = ERRSTR_STATUS_ERROR
            self.errUserName += ERRSTR_LONG_FIELD_20

        # CHECK for SPACES (find returns -1 if not found)
        if self.strUserName.find(" ") > -1:
            isSuccess = False
            self.ssUserName = ERRSTR_STATUS_ERROR
            self.errUserName += ERRSTR_SPACES_FIELD

        # CHECK for UNIQUE
        if BlogzUser.query.filter_by( handle = self.strUserName ).options( load_only("handle") ).first() != None:
            isSuccess = False
            self.ssUserName = ERRSTR_STATUS_ERROR
            self.errUserName += ERRSTR_USER_EXIST

        for i in range(len(self.strUserPass)):
            # CHECK for EMPTY
            if self.strUserPass[i] == "":
                isSuccess = False
                self.ssUserPass[i] = ERRSTR_STATUS_ERROR
                self.errUserPass[i] += ERRSTR_EMPTY_FIELD
            
            # CHECK for LENGTH
            if len(self.strUserPass[i]) < 3:
                isSuccess = False
                self.ssUserPass[i] = ERRSTR_STATUS_ERROR
                self.errUserPass[i] += ERRSTR_SHORT_FIELD_3

            if len(self.strUserPass[i]) > 20:
                isSuccess = False
                self.ssUserPass[i] = ERRSTR_STATUS_ERROR
                self.errUserPass[i] += ERRSTR_LONG_FIELD_20

        # CHECK for MATCH
        if self.strUserPass[0] != self.strUserPass[1]:
            isSuccess = False
            for i in range(len(self.strUserPass)):
                self.ssUserPass[i] = ERRSTR_STATUS_ERROR
                self.errUserPass[i] = ERRSTR_MATCH_FIELD

        # CHECK for EMPTY
        if self.strUserEmail == "":
            isSuccess = False
            self.ssUserEmail = ERRSTR_STATUS_ERROR
            self.errUserEmail = ERRSTR_EMPTY_FIELD

        # CHECK for SPACES (find returns -1 if not found)
        if self.strUserEmail.find(" ") > -1:
            isSuccess = False
            self.ssUserEmail = ERRSTR_STATUS_ERROR
            self.errUserEmail += ERRSTR_SPACES_FIELD
            
        # CHECK for @
        if self.strUserEmail.find("@") == -1:
            isSuccess = False
            self.ssUserEmail = ERRSTR_STATUS_ERROR
            self.errUserEmail += ERRSTR_INVALID_EMAIL

        # Check for LENGTH
        if len(self.strUserEmail) < 3:
            isSuccess = False
            self.ssUserEmail = ERRSTR_STATUS_ERROR
            self.errUserEmail += ERRSTR_SHORT_FIELD_3

        if len(self.strUserEmail) > 127:
            isSuccess = False
            self.ssUserEmail = ERRSTR_STATUS_ERROR
            self.errUserEmail += ERRSTR_LONG_FIELD_127

        # CHECK for UNIQUE
        if BlogzUser.query.filter_by( handle = self.strUserName ).options( load_only("email") ).first() != None:
            isSuccess = False
            self.ssUserName = ERRSTR_STATUS_ERROR
            self.errUserName += ERRSTR_EMAIL_EXIST

        return isSuccess

# ROUTE 'signup' :: User Signup -- separates POST / GET logic : Redundant Blacklist
@app.route( "/signup", methods=['POST','GET'] )
def signup( ):
    # BUILD nav string
    strNav = strNav_base + " :: " + '<a href="/signup">' + ghPAGE_SIGNUP + '</a>'
    
    # POST condition
    if request.method == 'POST':
        #NOTE: error checking aggregates and falls through

        # Init Signup Validator
        vtor = ValidateSignup( request.form['inUserName'], request.form['inUserPass0'], request.form['inUserPass1'], request.form['inUserEmail'] )
        isValid = vtor.isValid()
                
        if isValid:
            # default level is 1
            new_user = BlogzUser( vtor.strUserName, vtor.strUserPass[0], vtor.strUserEmail, 1 )
            db.session.add(new_user)
            db.session.commit()
            # TODO redirect to an interrim info page?
            return redirect('login', 302)

        else:
            return render_template('signup.html',ghSite_Name=ghSITE_NAME,ghPage_Title=ghPAGE_SIGNUP,ghSlogan=getSlogan(),ghUser_Name=get_current_user(),ghUser_Menu=Markup(get_user_menu),ghNav=Markup(strNav),strUserName=vtor.strUserName,strUserEmail=vtor.strUserEmail,statusUserName=vtor.ssUserName,statusUserPass0=vtor.ssUserPass[0],statusUserPass1=vtor.ssUserPass[1],statusUserEmail=vtor.ssUserEmail,strerrUserName=vtor.errUserName,strerrUserPass0=vtor.errUserPass[0],strerrUserPass1=vtor.errUserPass[1],strerrUserEmail=vtor.errUserEmail,ghErratae=get_fetch_info() )
            
    return render_template('signup.html',ghSite_Name=ghSITE_NAME,ghPage_Title=ghPAGE_SIGNUP,ghSlogan=getSlogan(),ghUser_Name=get_current_user(),ghUser_Menu=Markup(get_user_menu()),ghNav=Markup(strNav),ghErratae=get_fetch_info() )

# ROUTE "/newpost" :: Create a new blog entry : Restricted Blacklist
@app.route( "/newpost", methods=['POST', 'GET'] )
def newpost( ):
    strNav = strNav_base + " :: " + '<a href="/blog">' + ghPAGE_NEWPOST + '</a>'

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
            return render_template('newpost.html',ghSite_Name=ghSITE_NAME,ghPage_Title=ghPAGE_NEWPOST,ghSlogan=getSlogan(),ghUser_Name=get_current_user(),ghUser_Menu=Markup(get_user_menu()),ghNav=Markup(strNav),ghErratae=get_fetch_info(), vTitle=strTitle, vEntry=strEntry, strerrTitle=strerrTitle, strerrEntry=strerrEntry )
        
        #if success
        owner = BlogzUser.query.filter_by(handle=session['handle']).first()
        new_post = BlogzEntry( owner, strTitle, strEntry )
        db.session.add( new_post )
        db.session.commit()

        #TODO update owner with new post

        return redirect('blog?id='+str(new_post.id), 302)
    
    return render_template('newpost.html',ghSite_Name=ghSITE_NAME,ghPage_Title=ghPAGE_NEWPOST,ghSlogan=getSlogan(),ghUser_Name=get_current_user(),ghUser_Menu=Markup(get_user_menu),ghNav=Markup(strNav),ghErratae=get_fetch_info() )

def main():
    app.run()

if __name__ == "__main__":
    main()
