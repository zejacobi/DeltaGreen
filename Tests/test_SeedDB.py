import json
import unittest
from threading import Thread

import mongomock
import os

import SeedDB as SeedDB

test_file = os.path.join('.', 'Tests', 'TestData', 'test.json')
json_obj = {"_id": "test"}


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """generate the JSON file"""
        with open(test_file, 'w+') as file_obj:
            file_obj.write(json.dumps(json_obj))

    @classmethod
    def tearDownClass(cls):
        """remove the JSON file"""
        os.remove(test_file)

    def setUp(self):
        self.SeedDB = SeedDB
        self.mongo = mongomock.MongoClient()['Test']
        self.SeedDB.Mongo.database = self.mongo

    def test_worker(self):
        """Ensure that the worker function can insert JSON into the database"""
        self.SeedDB.q.put(test_file)
        t = Thread(target=self.SeedDB.worker)
        t.start()
        self.SeedDB.q.join()
        self.SeedDB.q.put(None)
        t.join()
        self.assertEqual(self.mongo['test'].find()[0], {"_id": 'test'})
