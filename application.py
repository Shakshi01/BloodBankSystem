import logging
import sqlite3
import tkinter
from datetime import date
from sqlite3.dbapi2 import Cursor
from tkinter import *
from tkinter import messagebox, scrolledtext, ttk
from PIL import Image, ImageTk
from DataBaseCreation import createDatabase
from HashSaltPassword import *
createDatabase()

#Logging the Data into the BloodBanklogfile
logging.basicConfig(filename='BloodBanklogfile.log',level=logging.INFO,format='%(asctime)s:%(levelname)s:%(lineno)d:%(funcName)s:%(message)s')

