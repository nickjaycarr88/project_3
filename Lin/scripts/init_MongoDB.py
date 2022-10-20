import pymongo

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

client.drop_database('db')

db = client.db

collector=[]






db.insert_many(collector)