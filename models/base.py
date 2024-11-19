# models/base.py
from abc import ABC, abstractmethod
from bson import ObjectId

class BaseModel(ABC):
    def __init__(self, db):
        self.db = db
        self.collection = self.get_collection()

    @abstractmethod
    def get_collection(self):
        pass

    def create(self, data):
        return self.collection.insert_one(data)

    def find_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def update(self, id, data):
        return self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )

    def delete(self, id):
        return self.collection.delete_one({"_id": ObjectId(id)})