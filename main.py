from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import NewUser

from util import create_user_id
from data import users
import time
import logging

app=FastAPI()

logging.basicConfig(filename="requests.log",  level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")

async def log_time_taken(request: Request, call_next):
    start = time.perf_counter_ns()
    response = await call_next(request)
    end = time.perf_counter_ns()
    request_time = end-start


    seconds = request_time // 1000000000
    milliseconds = (request_time % 1000000000) // 1000000

    print(f"{request.method} {request.url.path} took {seconds} seconds and {milliseconds} milliseconds")
    logging.info(f"{request.method} {request.url.path} took {seconds} seconds and {milliseconds} milliseconds")

    return response

app.middleware("http")(log_time_taken)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/signup", status_code=201)
async def create_user(new_user: NewUser):
    user_data = new_user.model_dump()
    if any(user["email"] == user_data["email"] for user in users.values()):
        raise HTTPException(status_code=409, detail="Email already registered!")

    user_id = create_user_id()
    users[user_id] = new_user.model_dump()

    return {"message": "Sign up successful", "data":new_user}
