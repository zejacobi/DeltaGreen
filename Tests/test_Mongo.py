import unittest
import mongomock

import Lib.Mongo as Mongo


class TestInsert(unittest.TestCase):
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


class TestFind(unittest.TestCase):
    def setUp(self):
        self.Mongo = Mongo
        self.collection = 'Test'
        self.mongo = mongomock.MongoClient()[self.collection]
        self.Mongo.database = self.mongo
        self.insertedDocs = [dict(_id=1, data=1), dict(_id=2, data=2), dict(_id=3, data=3)]
        self.mongo[self.collection].insert_many(self.insertedDocs)

    def test_mock(self):
        """Ensure that the database has been successfully mocked"""
        self.assertEqual(self.Mongo.database.client.address, ('localhost', 27017))

    def test_find_all(self):
        """Ensure that find_all returns all inserted records"""
        self.assertEqual(Mongo.find_all(self.collection), self.insertedDocs)

    def test_find_subset(self):
        """Ensure that find_subset returns one the expected results"""
        self.assertEqual(Mongo.find_subset(self.collection, {'_id': {'$lte': 2}}),
                         self.insertedDocs[0:2])

    def test_find_one(self):
        """Ensure that find_one returns the expected document if given no query"""
        self.assertEqual(Mongo.find_one(self.collection), {'data': self.insertedDocs[0]['data']})

    def test_find_one_with_query(self):
        """Ensure that find_one returns the expected document if given a query"""
        self.assertEqual(Mongo.find_one(self.collection, {'data': 2}),
                         {'data': self.insertedDocs[1]['data']})
