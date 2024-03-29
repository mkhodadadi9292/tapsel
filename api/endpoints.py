from typing import List
from fastapi import HTTPException, Query, Depends
from pymongo import MongoClient, ASCENDING
from cachetools import TTLCache
from schema import AdData, StatModel
from dependencies import get_mongo_db
from setting import CTR_collection, stats_collection
from middlewares import app

cache = TTLCache(maxsize=100, ttl=60)


@app.on_event("startup")
async def startup_event():
    _db = get_mongo_db()
    _db[stats_collection].create_index([("response_time", ASCENDING)])


@app.get("/predict", summary="Get all related CRVs.", response_model=List[AdData])
async def predict(ids: List[int] = Query(..., title="List of primary keys"),
                  db: MongoClient = Depends(get_mongo_db)):
    """
    Get all related CRVs
    :param ids: adIds
    :return: list of related CRVs data.
    """
    cache_key = f"predict_result_{hash(tuple(ids))}"
    cached_result = cache.get(cache_key)

    if cached_result:
        return cached_result

    query_result = db[CTR_collection].find({"adId": {"$in": ids}})
    result = [AdData(**item) for item in query_result]
    cache[cache_key] = result
    return result


@app.get("/stats", response_model=StatModel)
async def get_stats(db: MongoClient = Depends(get_mongo_db)):
    """
    Retrieve general statistics from the MongoDB collection.
    :return: general statistics
    """

    pipeline = [
        {
            "$group": {
                "_id": None,
                "count": {"$sum": 1},
                "avg_response_time": {"$avg": "$response_time"},
                "p99_response_time": {"$percentile": {"input": "$response_time", "p": [0.99], "method": 'approximate'}}
            }
        }
    ]

    stats = list(db[stats_collection].aggregate(pipeline))[0]
    stats['p99_response_time'] = stats['p99_response_time'][0]
    return stats
