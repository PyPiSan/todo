from flask import Flask, Response
from pymongo import MongoClient
from datetime import date, datetime
import json
from bson import json_util
import os

app = Flask(__name__)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

# try:
#     # print(client.server_info())
#     db = client.Todo
#     collection = db.todo
# except Exception:
#     print("Unable to connect to the server.")  

# todo1 = {
#         "title": "My first todo!",
#         "subject": "To learn MogoDB, PyMongo, Redis and other things",
#         "date": datetime.datetime.utcnow()}
# todo_id = db.todo.insert_one(todo1).inserted_id
# print(todo_id)

# To implement CRUD on MongoDB
class MongoConnect:
    def __init__(self, data):
        conn_str = os.environ["CODE"]
        self.client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
        # database = data['database']
        # collection = data['collection']
        cursor = self.client.Todo
        self.collection = cursor.todo
        self.data = data

    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output


    def write(self, data):
        # log.info('Writing Data')
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output


    def update(self):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output



@app.route('/', methods=['GET'])
def home():
    data = {}
    obj = MongoConnect(data)
    response = obj.read()
    response=json.dumps(response, default=json_util.default)
    return Response(response)
    

if __name__ == "__main__":
    app.run(debug=True, port = 8000, host='0.0.0.0')
