import unittest
import os
import mongomock
import json

from threading import Thread

import SeedDB as SeedDB

test_file = os.path.join('.', 'Tests', 'TestData', 'test.json')
json_obj = {"_id": "test"}


class TestParsingJSON(unittest.TestCase):
    """Test the JSON parsing"""
    @classmethod
    def setUpClass(cls):
        """generate the JSON file"""
        with open(test_file, 'w+') as file_obj:
            file_obj.write(json.dumps(json_obj))

    @classmethod
    def tearDownClass(cls):
        """remove the JSON file"""
        os.remove(test_file)

    def test_parse_json(self):
        obj, name = SeedDB.parse_json(test_file)
        self.assertDictEqual(obj, json_obj)
        self.assertEqual(name, 'test')


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
        self.SeedDB.database = self.mongo

    def test_mock(self):
        """Ensure that the database has been successfully mocked"""
        self.assertEqual(self.SeedDB.database.client.address, ('localhost', 27017))

    def test_insert(self):
        """Ensure that the insert function works"""
        self.assertEqual(self.SeedDB.insert({"_id": "test"}, 'test'), 'test')  # give back _id
        self.assertEqual(self.mongo['test'].find()[0], {"_id": 'test'})  # inserted the record

    def test_worker(self):
        """Ensure that the worker function can insert JSON into the database"""
        self.SeedDB.q.put(test_file)
        t = Thread(target=self.SeedDB.worker)
        t.start()
        self.SeedDB.q.join()
        self.SeedDB.q.put(None)
        t.join()
        self.assertEqual(self.mongo['test'].find()[0], {"_id": 'test'})  # inserted the record
