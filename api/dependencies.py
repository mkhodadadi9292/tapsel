from setting import mongo_uri, database_name
from pymongo import MongoClient

# client = MongoClient(mongo_uri)
# db = client[database_name]


#
# def get_mongo_db(collection_name):
#     def inner():
#         collection = db[collection_name]
#         return collection
#
#     return inner

def get_mongo_db():
    client = MongoClient(mongo_uri)
    db = client[database_name]
    return db
