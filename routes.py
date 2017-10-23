"""Provide routes for BLOGz"""
# routes.py
# Build A Blog :: routes
# 2017, polarysekt

import os

from flask import Flask, request, redirect, render_template, session
from flask import Markup, url_for, send_from_directory
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy.orm import load_only

from app import app, db, valid_session_key

from models import BlogzUser, BlogzEntry
from strings import *
from helpers import *

from gh_slogan import getSlogan
from gh_poker import get_demo


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
            return redirect("login?target="+request.endpoint, 302)
    else:
        # Check for redundancy (logged users trying to relog or create)
        redundant_routes = ['login', 'signup']
        if request.endpoint in redundant_routes:
            return redirect("/", 302)

# Provide a favicon.ico (compatible)
@app.route("/favicon.ico")
def static_favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

# Provide style.css
@app.route("/style.css")
def static_style():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'style.css')

@app.route("/gh_bbcode.js")
def static_gh_bbcode():
    return send_from_directory(os.path.join(app.root_path, 'static/script'), 'gh_bbcode.js')

@app.route("/nvp.js")
def static_nvp():
    return send_from_directory(os.path.join(app.root_path, 'static/script'), 'nvp.js')


# ROUTE: '/' :: Main Site Index : open access
@app.route("/")
def index():

    view_users = BlogzUser.query.options(load_only("handle", "email", "level"))

    return render_template('index.html', ghPage_Title=ghPAGE_HOME, ghSlogan=Markup(getSlogan()), ghUser_Name=get_current_user(), ghNav=Markup(strNav_base), ghErratae=Markup(get_fetch_info()), ghUsers=view_users)

# ROUTE: '/blog' :: Blog View Page : open access
@app.route("/blog")
#@app.route("/blog/<int:page>")
def blog():
    strNav = strNav_base + " :: " + '<a href="/blog">' + ghPAGE_BLOG + '</a>'

    # DETERMINE view TYPE
    strUserName = request.args.get('user')
    intViewId = request.args.get('id', type=int, default=0)
    intLimit = request.args.get('limit', type=int, default=5)
    page = request.args.get(get_page_parameter(), type=int, default=1)

    if strUserName:
        #Get owner_id
        #TODO load_only?
        owner_row = BlogzUser.query.filter_by(handle=strUserName).first()
        if owner_row:
            intOwnerId = owner_row.id
        else:
            intOwnerId = 0
        strNav += ' :: <a href="?user=' + strUserName + '">' + strUserName + "</a>"
        if intViewId > 0:
            strNav += ' & <a href="?id=' + strViewId + '">id=' + strViewId + '</a>'
            view_entries = BlogzEntry.query.filter_by(owner_id=intOwnerId, id=intViewId).paginate(page,intLimit)
        else:
            view_entries = BlogzEntry.query.filter_by(owner_id=intOwnerId).paginate(page,intLimit)
    else:
        if intViewId > 0:
            strNav += ' :: <a href="?id=' + strViewId + '">id=' + strViewId + '</a>'
            view_entries = BlogzEntry.query.filter_by(id=intViewId).paginate(page,intLimit)
        else:
            strNav += ' :: <a href="blog">all</a>'
            view_entries = BlogzEntry.query.paginate(page,intLimit)


    #convert the dates to local server time
    #TODO get users local time?
    for i in view_entries.items:
        i.created = gh_getLocalTime(i.created)

    return render_template('blog.html', limit=intLimit,ghPage_Title=ghPAGE_BLOG, ghSlogan=Markup(getSlogan()), ghUser_Name=get_current_user(), ghNav=Markup(strNav), ghErratae=Markup(get_fetch_info()), ghEntries=view_entries)

# ROUTE '/login' :: User Login Page : Redundancy Blacklist
@app.route("/login", methods=['POST', 'GET'])
def login():
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
                rowUserEntry = BlogzUser.query.filter_by(handle=strUserName).first()
                if rowUserEntry:
                    # CHECK PASSWORD
                    if bcrypt.check_password_hash(rowUserEntry.pass_hash, strUserPass):

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

    return render_template('login.html', ghPage_Title=ghPAGE_LOGIN, ghSlogan=Markup(getSlogan()), ghUser_Name=get_current_user(), ghNav=Markup(strNav), vUserName=strUserName, statusUserName=ssUserName, strerrUserName=strerrUserName, statusUserPass=ssUserPass, strerrUserPass=strerrUserPass, ghErratae=Markup(get_fetch_info()))

# ROUTE '/logout' :: User Logout / End Session : Restricted Blacklist
@app.route("/logout")
def logout():
    del session[valid_session_key]
    del session['loglevel']
    del session['handle']
    return redirect("/", 302)

# ROUTE 'signup' :: User Signup -- separates POST / GET logic : Redundant Blacklist
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    # BUILD nav string
    strNav = strNav_base + " :: " + '<a href="/signup">' + ghPAGE_SIGNUP + '</a>'

    # POST condition
    if request.method == 'POST':
        #NOTE: error checking aggregates and falls through

        # Init Signup Validator
        vtor = ValidateSignup(request.form['inUserName'], request.form['inUserPass0'], request.form['inUserPass1'], request.form['inUserEmail'])
        isValid = vtor.isValid()

        if isValid:
            # default level is 1
            new_user = BlogzUser(vtor.strUserName, vtor.strUserPass[0], vtor.strUserEmail, 1)
            db.session.add(new_user)
            db.session.commit()
            # TODO redirect to an interrim info page?
            return redirect('login', 302)
        else:
            return render_template('signup.html', ghPage_Title=ghPAGE_SIGNUP, ghSlogan=Markup(getSlogan()), ghUser_Name=get_current_user(), ghNav=Markup(strNav), strUserName=vtor.strUserName, strUserEmail=vtor.strUserEmail, statusUserName=vtor.ssUserName, statusUserPass0=vtor.ssUserPass[0], statusUserPass1=vtor.ssUserPass[1], statusUserEmail=vtor.ssUserEmail, strerrUserName=vtor.errUserName, strerrUserPass0=vtor.errUserPass[0], strerrUserPass1=vtor.errUserPass[1], strerrUserEmail=vtor.errUserEmail, ghErratae=Markup(get_fetch_info()))

    return render_template('signup.html', ghPage_Title=ghPAGE_SIGNUP, ghSlogan=Markup(getSlogan()), ghUser_Name=get_current_user(), ghUser_Menu=Markup(get_user_menu()), ghNav=Markup(strNav), ghErratae=Markup(get_fetch_info()))

# ROUTE "/newpost" :: Create a new blog entry : Restricted Blacklist
@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
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
        if strTitle == "":
            isSuccess = False
            strerrTitle = "Post must contain a title"

        if strEntry == "":
            strerrEntry = "Post must contain an entry"
            isSuccess = False

        if not isSuccess:
            return render_template('newpost.html', ghPage_Title=ghPAGE_NEWPOST, ghSlogan=Markup(getSlogan()), ghUser_Name=get_current_user(), ghNav=Markup(strNav), ghErratae=get_fetch_info(), vTitle=strTitle, vEntry=strEntry, strerrTitle=strerrTitle, strerrEntry=strerrEntry)

        #if success
        owner = BlogzUser.query.filter_by(handle=session['handle']).first()
        new_post = BlogzEntry(owner, strTitle, strEntry)
        db.session.add(new_post)
        db.session.commit()

        #TODO update owner with new post

        return redirect('blog?id='+str(new_post.id), 302)

    return render_template('newpost.html', ghPage_Title=ghPAGE_NEWPOST, ghSlogan=Markup(getSlogan()), ghUser_Name=get_current_user(), ghNav=Markup(strNav), ghErratae=Markup(get_fetch_info()))

# ROUTE "/poker" is EASTER EGG
@app.route("/poker")
def poker():
    strNav = strNav_base + " :: "  + '<a href="/poker">' + ghPAGE_POKER + '</a>'
    intPlayers = 1

    strPlayers = request.args.get('playercount')

    if strPlayers:
        try:
            intPlayers = int(strPlayers)
        except:
            intPlayers = 1

        if intPlayers > 10:
            intPlayers = 10

        if intPlayers < 1:
            intPlayers = 1

    strNav += " :: " + str(intPlayers) + " Players"

    return render_template('poker.html', ghPage_Title=ghPAGE_POKER, ghSlogan=Markup(getSlogan()), ghUser_Name=get_current_user(), ghNav=Markup(strNav), ghPokerGame=Markup(get_demo(intPlayers)), ghPokerNumPlayers=intPlayers, ghErratae=Markup(get_fetch_info()))

@app.route("/test")
def route_test():
    return render_template('test.html')