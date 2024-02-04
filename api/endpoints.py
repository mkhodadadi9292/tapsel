from typing import List
from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from schema import AdData
from setting import mongo_uri, database_name, collection_name

app = FastAPI()

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]


@app.get("/predict", summary="Get all related CRVs.")
async def predict(ids: list[int] = Query(..., title="List of primary keys")) -> List[AdData]:
    query_result = collection.find({"adId": {"$in": ids}})
    return [AdData(**item) for item in query_result]


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
