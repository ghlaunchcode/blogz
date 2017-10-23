""" Entry point for BLOGz """
# main.py

from app import app
from routes import *

def main():
    app.run()

if __name__ == "__main__":
    main()
