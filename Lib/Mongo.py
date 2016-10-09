from pymongo import MongoClient
from DeltaGreen.ExternalServices import DATABASE, MONGO_STRING

client = MongoClient(MONGO_STRING + DATABASE)
database = client[DATABASE]
