"""
Using a separate file for the test app allows me to add in any mocks I might wish.
"""
import mongomock

import API.v1 as APIV1
import Lib.Utilities.Mongo as Mongo

from flask import Flask

from Tests.RandomMock import RandomMock

URL_PREFIX = '/tests/api/v1'

TEST_MONGO = Mongo
RANDOM_MOCK = RandomMock()
mongo_mock = mongomock.MongoClient()['Test']
TEST_MONGO.database = mongo_mock
APIV1.Character.Mongo = TEST_MONGO
APIV1.Generator.Mongo = TEST_MONGO
APIV1.Generator.Character.random = RANDOM_MOCK

app = Flask(__name__)

app.register_blueprint(APIV1.V1, url_prefix=URL_PREFIX)


if __name__ == "__main__":
    app.run('localhost', port=1000, debug=True)
