#! /usr/bin/python3

# app.py
# Build A Blog
# 2017, polarysekt

# imports
from flask import Flask, Markup, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

from gh_slogan import getSlogan


app = Flask( __name__ )
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#g_app.config['SQLALCHEMY_ECHO' ] = True

db = SQLAlchemy(app)


ghSITE_NAME = "BLOGz"

# ROUTE: '/' :: Main Site Index
@app.route( "/" )
def index( ):
    return render_template('index.html', ghSite_Name=ghSITE_NAME, ghPage_Title="Home", ghSlogan=getSlogan(), ghUser_Name=request.remote_addr)

# ROUTE: '/blog' :: Blog View Page
@app.route( "/blog" )
def blog( ):
    return render_template('blog.html', ghSite_Name=ghSITE_NAME, ghPage_Title="Blog Entries", ghSlogan=getSlogan() )

@app.route( "/login" )
def login( ):
    return render_template('login.html', ghSite_Name=ghSITE_NAME, ghPage_Title="Login", ghSlogan=getSlogan() )

@app.route( "/logout" )
def logout( ):
    #TODO
    return redirect( "/", 302 )

@app.route( "/signup" )
def signup( ):
    return render_template('signup.html', ghSite_Name=ghSITE_NAME, ghPage_Title="User Signup", ghSlogan=getSlogan() )

@app.route( "/newpost" )
def newpost( ):
    return render_template('newpost.html', ghSite_Name=ghSITE_NAME, ghPage_Title="New Post", ghSlogan=getSlogan() )

def main():
    app.run()

if __name__ == "__main__":
    main()
