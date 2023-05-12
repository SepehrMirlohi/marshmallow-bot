import time, json, os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path) 
from datetime import datetime
from database.db import DB




def add_inviter_info(info: dict):
    database = DB("invites")
    database.AddOneData(info)

def give_invites_list():
    database = DB('invites')
    return database.GetAllData()

