Quick Start
===========

The quick start is now even quicker!

Initialize Project
------------------

The project init is now very streamlined and automatic.

Unmentioned dependencies include: \* sh, bash (for scripts) \* virtualenv (for creating the virtual environment) \* python3 (for the app itself) \* pip3 (for app dependencies) \* libffi-dev (for certain dependencies) \* MySQL server, client, CLI (for the database) \* \* mariaDB should work as well (providing mysql interfaces) \* asciidoc, pandoc (for converting asciidoc to markdown) \* xfce4-terminal (for gui scripts)

### GUI script

> **Note**
>
> requires xfce4-terminal I could have generalized more, but the command line options differed.

`$ gui_init_all`

### Script

`$ util/init_all`

Run the server
--------------

Before the application will work, a server needs started.

This server will listen at port 5000 by default.

This is accessible via:

`http://localhost:5000`

or

`http://127.0.0.1:5000`

on simpler browsers, like *dillo*, *links*, *lynx*, etc.

### GUI

`$ gui_start_server`

### Script

\#TODO!

### Manual

`$ . mega/bin/activate`

> **Note**
>
> The first period "." is necessary, and there IS a space after. The *source* command can be used instead.

Old Quick Start
===============

Will require password for MySQL *root*

`$ util/init_all`

Initializes: \* schema (db) \* user / roles \* virtual environment *mega* \* python dependencies \* BlogzEntry \* BlogzUser \* Creates a *root* user for BlogzUser

Initialize the Virtual Environment
==================================

In lieu of using something like *anaconda*, the virtual environment is created manually.

The initenv script located in the util folder should do the trick.

`$ util/init_virtualenv`

Create DATABASE
===============

Using Script
------------

The database (and user) can now be created with a simple script.

`$ util/init_dbenv`

This script executes queries (3, actually) in util/createdb.sql.

> **Note**
>
> the script assumes a user *root*, and will require entry of that password.

(Simply hardcoding the password is very bad practice and would be recorded in bash history)

Using .sql file
---------------

Redirect the file into the mysql client CLI:

`$ mysql -u root -p < util/createdb.sql`

Using mysql-workbench
---------------------

-   Login to MySQL server "MySQL@localhost:3306" using user "root" and the correct authentication

-   \* Password may be a string or stored already in keychain

-   Create a new schema in the connected server

-   \* Set the name to blogz

-   \* Set default collation to utf8-default

`` CREATE SCHEMA `blogz `` DEFAULT CHARACTER SET utf8 ;\`

-   Create a new user

-   \* Set the name to "blogz"

-   \* Set the Limit to Hosts matching "localhost" or "127.0.0.1"

-   \* Set the password to "blogz"

-   \* Create a new schema privilege definition for "blogz"

-   \* \* Set ALL (for now)

Create initial TABLES
=====================

If the dependencies are only available to the virtual environment, fire that up

Using util script
-----------------

`$ util/init_models`

The virtual environment will be handled automatically.

> **Note**
>
> this requires the virtual environment as well as the db/user and the python dependencies.

`$ util/init_dbenv` `$ util/init_virtualenv` `$ util/init_pydep`

> **Note**
>
> the init\_models does not yet check for redundancy (yet: TODO!)

Using models.py
---------------

> **Note**
>
> this is the manual way. The virtual environment is required.

`$ python models.py`

Using CLI
---------

Open python CLI: `$ python3`

> **Note**
>
> python3 is specifically called in case `python` points to a different version.

`>>> from app import db` CREATE the TABLES `>>> from models import BlogzUser, BlogzEntry` `>>> db.create_all()`

CREATE a root user with a high loglevel (and simple password): `>>> new_user = BlogzUser( "root", "root" "root@localhost", 7 )` `>>> db.session.add( new_user )` `>>> db.session.commit()`

Old Walkthru
============

`$ source mega/bin/activate`

`$ util/init_pydep` (if dependencies required)

`$ python app.py`

Starting Over
=============

GUI Script
----------

`$ ./gui_rm_all`

Script
------

`$ /util/rm_all`

Dev-Related
===========

Dependencies
------------

The dependencies for the app are now located in a requirements file called *depends*.

This will be passed to the virtual environment 'mega’s pip3.

`$ util/init_pydep`

> **Note**
>
> this requires the virtual environment (mega).

Initialize that environment with

`$ util/init_virtualenv`

Templates
---------

Located in the *templates* folder

Static
------

There are currently no static data. Styles have been inlined to avoid caching for development and favicon is (will be) a route view.

Variables
---------

There are many important variables.

-   ghDEBUG (bool) to enable/disable debugging (including print() outputs)

-   Template Variables passed to render\_template()

-   Organizational Variables to avoid hardcoding

\#TODO: these are deprecated!!!

ghSite\_Name ghPage\_Title

The database
------------

\#TODO: there is still some finalization to be done to the models!!!

The database should be called blogz and accessible by user blogz.

For simplicity, the password is *blogz*.

> **Note**
>
> only should be accessible by localhost.

To Initialize the database and user with proper privileges (for localhost):

`$ util/init_dbenv`

To create the actual models (tables), use:

`$ util/init_models`

Please note this requires the virtual environment and the python dependencies:

`$ util/init_virtualenv && util/init_pydep`

Routes
------

There are a few ways to handle access: \* Allowed Routes (whitelist) \* \* Must be updated for new routes \* \* DON’T FORGET *favicon.ico* IS A ROUTE \* Restricted Routes (blacklist) \* \* Possibly more easily implemented \* \* Also used when routes are *redundant*, like a login or register when a user is already in!

Instead of creating a *singleUser* route for posts, this is handled with GET requests.

/blog

-   id : integer \> 0, otherwise no return

-   user : valid user, otherwise no return

These can be used together with manual URI entry and will properly limit. However there is no actual link tag to provide this functionality.

For example:

`blog?id=5&user=root`

Will only return post id=5 if it is by the specified user.

-   limit : integer \>= 0, where 0 is NO LIMIT

-   page : integer : used when limit is specified

Date and Time
-------------

These are a bit of a pickle.

All dates and times are stored on the server in UTC.

Currently, these are converted to server local time when displayed, but ideally would adapt to user’s time zone (and DST)

Password Hashing
----------------

Currently just a simple hash is created using bcrypt.

This is then decoded into utf-8.

This results in a 60-byte hash that is stored instead of the password itself.

Additionally, care is taken to only use necessary columns when enumerating users.

Slogan
------

Once again, brought in the gh\_slogan module.

