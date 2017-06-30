"""
Script to get all of the JSON files into the Mongo Database
"""

import sys
import os

import Lib.Mongo as Mongo

from threading import Thread
from queue import Queue
from glob import glob

from Lib.Utilities.Workspace import parse_json

q = Queue()
num_threads = 2
threads = []


def worker():
    """
    Worker thread
    """
    while True:
        item = q.get()
        if item is None:
            break
        json_obj, collection_name = parse_json(item)
        Mongo.insert(json_obj, collection_name)
        q.task_done()

if __name__ == '__main__':
    try:
        directory = sys.argv[1]
    except IndexError:
        print('Error: No directory supplied.')
        exit()

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
