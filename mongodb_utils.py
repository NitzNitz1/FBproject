import os
from pymongo import MongoClient

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "database")

client = MongoClient("mongodb://localhost:27017/")
db = client[MONGO_DB_NAME]
collection = db["Jobs"]

def insert_job(job):
    return collection.insert_one(job)

def update_job(job_id, update_data):
    return collection.update_one({"_id": job_id}, {"$set": update_data})

def update_status(job_id, status):
    return collection.update_one({"_id": job_id}, {"$set": {"status": status}})

def find_job(job_id):
    return collection.find_one({"_id": job_id})

def find_fbid(username):
    return collection.find_one({"username": username, "fbid": {"$exists": True}})
