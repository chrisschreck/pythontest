from bson import ObjectId
from backend.mongodb import mydb


class Prescriptions():

    collection = mydb["Prescriptions"]
    def create(self, user_id, clinic_id, content):
        print(self.collection)
        insert = self.collection.insert_one({
            "user": user_id,
            "clinic": clinic_id,
            "content": content
        })
        if insert.acknowledged:
            print(insert.acknowledged)
            return insert.inserted_id

    def update(self, doc_id, content):
        tmp_old = self.get(doc_id)
        update = self.collection.update_one({'content': tmp_old["content"]}, {'$set': {'content': content}})
        if update.modified_count > 0:
            return True

    def get(self, doc_id):
        return self.collection.find_one({'_id': doc_id}, projection=None)

    def delete(self, doc_id):
        delete = self.collection.delete_one({'_id': doc_id})
        if delete.deleted_count > 0:
            return True

