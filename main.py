""" Entry point for BLOGz """
# main.py

import os

from app import app
from routes import *

def main():
    port = int(os.environ.get('PORT',5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
    
    
# vim:expandtabs ts=4 sw=4
