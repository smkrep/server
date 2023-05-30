from flask import Flask, request
from pydantic import BaseModel
from pymongo import MongoClient
from flask_cors import CORS

# class WishObj(BaseModel):
#     sberuserid: int
#     importance: str
#     name: str
#     price: int
#     category: str
#     additional_info: str

# class toUpdate(BaseModel):
#     sberuserid: str
#     list_of_wishes: list


app = Flask(__name__)
CORS(app)

@app.route("/")
def default():
    return "blank page"

@app.route("/api/getWishes/")
def get_wishes():
    args = request.args
    sberuserid = args.get('sberuserid')
    print(sberuserid)
    database = getDatabase()
    coll = database["SberWishes"]
    result = coll.find_one({'sberuserid': sberuserid}, {'_id': 0})
    print(result)
    return sberuserid


@app.route("/api/updateWishes/", methods=["POST"])
def update_wishes():
    request_data = request.get_json()
    sberuserid = None
    list_of_wishes = None

    if request_data:
        if 'sberuserid' in request_data:
            sberuserid = request_data['sberuserid']
        if 'list_of_wishes' in request_data:
            list_of_wishes = request_data['list_of_wishes']
    database = getDatabase()
    coll = database["SberWishes"]
    coll.update_one({'sberuserid': sberuserid}, {"$set": {'wishes': list_of_wishes}}, upsert=True)
    return request.get_json()

@app.route("/test/")
def test():
    return "test test test test"


def getDatabase():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = (
        "mongodb+srv://m2101760:LNndSjHPdxRWRDx4@wishes.a3tqmko.mongodb.net/SberWishes"
    )

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client["SberWishes"]
