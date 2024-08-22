import pymongo
import os
from bson.objectid import ObjectId

from todo_app.data.item import Item

def get_collection():
    client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTIONSTRING"))
    db = client[os.getenv('MONGODB_NAME')]
    collection = db[os.getenv("MONGODB_COLLECTION_NAME")]
    return collection


def get_items():
    items_collection = get_collection()
    items = items_collection.find()
    return [Item.from_mongo_document(item) for item in items]

def get_item(id):
    items_collection = get_collection()
    item = items_collection.find_one({"_id": ObjectId(id)})
    return Item.from_mongo_document(item) if item else None


def add_item(title, description, status):
    items_collection = get_collection()
    item = Item(id=None, name=title, status=status, desc=description)
    result = items_collection.insert_one(item.to_mongo_document())
    return str(result.inserted_id)


def save_item(item):
    items_collection = get_collection()
    items_collection.update_one(
        {"_id": ObjectId(item.id)},
        {"$set": {
            'name': item.name,
            'status': item.status,
            'desc': item.desc
        }}
    )
