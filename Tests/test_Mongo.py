import unittest
import mongomock

import Lib.Mongo as Mongo


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.Mongo = Mongo
        self.mongo = mongomock.MongoClient()['Test']
        self.Mongo.database = self.mongo

    def test_mock(self):
        """Ensure that the database has been successfully mocked"""
        self.assertEqual(self.Mongo.database.client.address, ('localhost', 27017))

    def test_insert(self):
        """Ensure that the insert function works for a dictionary"""
        self.assertEqual(self.Mongo.insert({"_id": "test"}, 'test'), 'test')
        self.assertEqual(self.mongo['test'].find()[0], {"_id": 'test'})

    def test_insert_single_dict_in_array(self):
        """Ensure that the insert function works for a single dict array"""
        self.assertEqual(self.Mongo.insert([{"_id": "test"}], 'test'), 'test')
        self.assertEqual(self.mongo['test'].find()[0], {"_id": 'test'})

    def test_insert_multi_dict_in_array(self):
        """Ensure that the insert function works for a single dict array"""
        ids = ['test', 'test1']
        dicts = [{"_id": ids[0]}, {"_id": ids[1]}]
        self.assertEqual(self.Mongo.insert(dicts, 'test'), ids)
        self.assertEqual(self.mongo['test'].find()[0], dicts[0])
        self.assertEqual(self.mongo['test'].find()[1], dicts[1])
