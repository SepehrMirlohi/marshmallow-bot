from dotenv import load_dotenv
from pymongo import MongoClient
import os, asyncio
load_dotenv()

#--------------------------------- Define variables ------------------------------------------
DB_URL = os.getenv('DB_URL')
DB_NAME = os.getenv('DB_NAME')


#-------------------------------------- Starting connection with Database ------------------------------

class DB():
    
    connection = MongoClient(DB_URL)

    def __init__(self, collection: str):
        
        # ---- Connecting to the database and find the collection
        self.db = self.connection[DB_NAME]
        self.collection = self.db[collection]



    def Databases(self):
        return self.connection.list_database_names()
    
    def Collections(self):
        return self.db.list_collection_names()
    
    def AddOneData(self, data: dict):
        
        result = self.collection.insert_one(data)
        if result:
            return True
        
    def AddListData(self, data: list):
        result = self.collection.insert_many(data)
        if result: 
            return True
        return False
    
    def GetOneData(self, condition: dict = None):
        result = self.collection.find_one(condition)
        if result: 
            return result
        return False

    def GetAllData(self, condition: dict = {}):
        result = self.collection.find()
        if result: 
            return result
        
    def RemoveData(self, condition: dict):
        result = self.collection.delete_one(condition)
        if result:
            return True
        return False
    
    def UpdateOne(self, condition: dict, new_data: dict):
        newValue = {"$set": new_data}
        result = self.collection.update_one(condition, newValue)
        if result:
            return True
        return False

    def UpdateWithPush(self, condition, new_data):
        result = self.collection.update_one(condition, {"$push": new_data})
        if result: 
            return True
        return False
    

