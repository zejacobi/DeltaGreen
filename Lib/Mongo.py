from pymongo import MongoClient
from ExternalServices import DATABASE, MONGO_STRING

client = MongoClient(MONGO_STRING)
database = client[DATABASE]
