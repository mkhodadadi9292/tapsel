from fastapi import HTTPException, Depends, Request, FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import time
from setting import mongo_uri, database_name, stats_collection

app = FastAPI()

client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[stats_collection]


@app.middleware("http")
async def update_stats(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    elapsed_time = end_time - start_time

    stats = {
        "endpoint": request.url.path,
        "timestamp": datetime.now(),
        "response_time": elapsed_time
    }
    collection.insert_one(stats)

    return response
