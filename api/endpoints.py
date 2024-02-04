from typing import List
from fastapi import HTTPException, Query
from pymongo import MongoClient
from schema import AdData, StatModel
from setting import mongo_uri, database_name, collection_name
from middlewares import app, collection as _collection

client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]


@app.get("/predict", summary="Get all related CRVs.", response_model=List[AdData])
async def predict(ids: list[int] = Query(..., title="List of primary keys")):
    query_result = collection.find({"adId": {"$in": ids}})
    return [AdData(**item) for item in query_result]


@app.get("/stats", response_model=StatModel)
async def get_stats():
    """
    Retrieve general statistics from the MongoDB collection.
    """

    pipeline = [
        {
            "$group": {
                "_id": None,
                "count": {"$sum": 1},
                "avg_response_time": {"$avg": "$response_time"}
            }
        }
    ]

    stats = list(_collection.aggregate(pipeline))[0]

    return stats
