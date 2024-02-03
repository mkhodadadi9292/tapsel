import csv
import json
from pymongo import MongoClient

# MongoDB connection settings
mongo_uri = "mongodb://mongodb:27017/"
database_name = "advertising"
collection_name = "CTR"


# CSV file path
csv_file_path = "./task-23-dataset.csv"

# Convert CSV to a list of dictionaries
data = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]


# Check if the collection exists, create it if not
if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)

collection = db[collection_name]



# Insert data into MongoDB
collection.insert_many(data)

# Close MongoDB connection
client.close()

print(f"Data from {csv_file_path} imported into MongoDB collection {collection_name}")
