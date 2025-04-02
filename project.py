from fastapi import FastAPI
from rabbitmq_utils import publish
from mongodb_utils import insert_job, find_job, find_fbid
from datetime import datetime
from facebook_utils import get_user_id
import uuid
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # או http://localhost:3000 אם בא לך לאבטח
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/job", tags=["Jobs"])
def create_job(username: str):
    job_id = str(uuid.uuid4())
    job = {
        "_id": job_id,
        "start_date": datetime.utcnow(),
        "end_date": None,
        "status": "READY",
        "success": None,
        "error_message": None,
        "fbid": None,
        "username": username
    }
    insert_job(job)
    publish(job_id, username)
    return {"message": "Job created successfully!", "job_id": job_id}

@app.get("/job/{job_id}", tags=["Jobs"])
def get_job(job_id: str):
    job = find_job(job_id)
    if job is None:
        return {"error": "Job not found"}, 404
    return job

@app.get("/fbid/{username}", tags=["FBID"])
def fbid_lookup(username: str):
    user_id = get_user_id(username)
    if user_id is None:
        return {"fbid": None, "success": False, "error": "User not found or inaccessible"}
    return {"fbid": user_id, "success": True}