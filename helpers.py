# helpers.py

import time
from datetime import datetime
import pytz
from tzlocal import get_localzone

from flask import session, request
from sqlalchemy.orm import load_only

from app import valid_session_key, ghDEBUG, bcrypt
from models import BlogzUser
from strings import *

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
