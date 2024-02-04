from typing import List
from fastapi import HTTPException, Query
from pymongo import MongoClient
from cachetools import TTLCache
from schema import AdData, StatModel
from setting import mongo_uri, database_name, collection_name
from middlewares import app, collection as _collection

client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

cache = TTLCache(maxsize=100, ttl=60)


@app.get("/predict", summary="Get all related CRVs.", response_model=List[AdData])
async def predict(ids: list[int] = Query(..., title="List of primary keys")):
    cache_key = f"predict_result_{hash(tuple(ids))}"
    cached_result = cache.get(cache_key)

    if cached_result:
        return cached_result

    query_result = collection.find({"adId": {"$in": ids}})
    result = [AdData(**item) for item in query_result]
    cache[cache_key] = result
    return result


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
