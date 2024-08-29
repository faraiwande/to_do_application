from bson.objectid import ObjectId

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