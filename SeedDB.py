"""
Script to get all of the JSON files into the Mongo Database
"""

import json
import sys
import os

from threading import Thread
from queue import Queue
from glob import glob


from Lib.Mongo import database

q = Queue()
num_threads = 2
threads = []


def insert(json_doc, collection):
    """
    Function for inserting JSON files into a database
    :param json json_doc: A valid JSON document
    :param str collection: The collection to insert the document into
    :return: The unique ID given to the inserted item
    """
    return database[collection].insert(json_doc)


def parse_json(json_file_path):
    """
    Parses a JSON file and returns the object encoded in it and the bare name of the file
    :param str json_file_path: A relative or absolute path from the current directory to a file in
        JSON format
    :return: A tuple containing an object in JSON format and a string containing the name of
        the file the JSON object was drawn from with the path and .json removed
    :rtype tuple
    """
    with open(json_file_path, 'r') as file_obj:
        raw_json = file_obj.read()
        json_obj = json.loads(raw_json)

    file_name = os.path.split(json_file_path)[1].replace('.json', '')
    return json_obj, file_name


def worker():
    """
    Worker thread
    """
    while True:
        item = q.get()
        if item is None:
            break
        json_obj, collection_name = parse_json(item)
        insert(json_obj, collection_name)
        q.task_done()

if __name__ == '__main__':
    directory = sys.argv[1]
    json_dir = os.path.join(os.curdir, directory)
    json_files = glob(json_dir + '*.json')

    for i in range(num_threads):
        t = Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    for file in json_files:
        q.put(file)

    q.join()

    for i in range(num_threads):
        q.put(None)
    for t in threads:
        t.join()
