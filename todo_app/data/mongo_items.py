import pymongo
import os
from bson.objectid import ObjectId

client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTIONSTRING"))
db = client[os.getenv("MONGODB_NAME")]
collection = db[os.getenv("MONGODB_COLLECTION_NAME")]

class Item:
    def __init__(self, id, name, status, desc):
        self.id = id
        self.name = name
        self.status = status
        self.desc = desc 

    @classmethod 
    def from_mongo_document(cls, doc):
        return cls(
            str(doc['_id']),
            doc['name'],
            doc['status'],
            doc.get('desc', '')
        )
    
    def to_mongo_document(self):
        return {
            '_id': ObjectId(self.id) if self.id else ObjectId(), 
            'name': self.name,
            'status': self.status,
            'desc': self.desc
        }

def get_items():
    items_collection = collection
    items = items_collection.find()
    return [Item.from_mongo_document(item) for item in items]

def get_item(id):
    items_collection = collection
    item = items_collection.find_one({"_id": ObjectId(id)})
    return Item.from_mongo_document(item) if item else None


def add_item(title, description, status):
    items_collection = collection
    item = Item(id=None, name=title, status=status, desc=description)
    result = items_collection.insert_one(item.to_mongo_document())
    return str(result.inserted_id)


def save_item(item):
    items_collection = collection
    items_collection.update_one(
        {"_id": ObjectId(item.id)},
        {"$set": {
            'name': item.name,
            'status': item.status,
            'desc': item.desc
        }}
    )
