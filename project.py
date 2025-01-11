import uuid
from datetime import datetime
import pika
from pymongo import MongoClient
from fastapi import FastAPI


client = MongoClient('mongodb://mongo:27017/')
db = client["database"]
collection = db["Jobs"]

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
channel = connection.channel()
channel.queue_declare(queue='job_queue', durable=True)

app = FastAPI()

@app.post("/job")
def create_job(username: str):
    print("creating job request")
    job_id = str(uuid.uuid4())
    start_date = datetime.utcnow()

    job = {
        "_id": job_id,
        "start_date": start_date,
        "end_date": None,
        "status": "READY",
        "success": None,
        "error_message": None,
        "fbid": None,
        "username": username,
    }
    collection.insert_one(job)

    channel.basic_publish(
        exchange='',
        routing_key='job_queue',
        body=f"{job_id},{username}",
        properties=pika.BasicProperties(
            delivery_mode=2,
    ))

    return {"job_id": job_id}

@app.get("/job/{job_id}")
async def get_job(job_id: str):
    job = collection.find_one({"_id": job_id})
    if job is None:
        return {"error": "Job not found"}, 404
    return job


@app.get("/fbid/{username}")
async def get_fbid(username: str):
    job = collection.find_one({"username": username, "fbid": {"$ne": None}})
    if job is None:
        return {"error": "User ID not found for this username"}, 404
    return {"fbid": job["fbid"]}




