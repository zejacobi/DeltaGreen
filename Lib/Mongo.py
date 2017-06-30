from pymongo import MongoClient
from ExternalServices import DATABASE, MONGO_STRING

client = MongoClient(MONGO_STRING + DATABASE)
database = client[DATABASE]


def insert(json_doc, collection):
    """
    Function for inserting JSON files into a Mongo database

    :param dict_or_list json_doc: A valid python dictionary or list, which will be converted to
        the MongoDB BSON format as it is inserted into the database.
    :param str collection: The collection to insert the document into
    :return: The unique ID or IDs given to the inserted item
    :rtype: string_or_list
    """
    if isinstance(json_doc, dict):
        return database[collection].insert_one(json_doc).inserted_id
    elif len(json_doc) == 1:
        return database[collection].insert_one(json_doc[0]).inserted_id
    else:
        return database[collection].insert_many(json_doc).inserted_ids
