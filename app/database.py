from pymongo import MongoClient
import urllib.parse
import os

MONGODB_DB = str(os.environ.get("MONGO_DB", default='kreacity'))
HOSTMONGO = str(os.environ.get("HOSTMONGO", default='127.0.0.1'))
MONGODB_PORT = int(os.environ.get("MONGODB_PORT", default=27017))

username = urllib.parse.quote_plus(os.environ.get("USERMONGO", default='test'))
password = urllib.parse.quote_plus(os.environ.get("PASSWORDMONGO", default='test'))

client = MongoClient(( 'mongodb://%s:%s@' % (username, password) ) + HOSTMONGO, MONGODB_PORT)
db = client[MONGODB_DB]
