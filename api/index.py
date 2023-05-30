from flask import Flask
from pydantic import BaseModel
from pymongo import MongoClient

class WishObj(BaseModel):
    sberuserid: int
    importance: str
    name: str
    price: int
    category: str
    additional_info: str

class toUpdate(BaseModel):
    sberuserid: str
    list_of_wishes: list


app = Flask(__name__)

@app.route("/")
def default():
    return "blank page"

@app.route("/api/getWishes/")
def get_wishes(sberuserid: str):
    database = getDatabase()
    coll = database["SberWishes"]
    result = coll.find_one({'sberuserid': sberuserid}, {'_id': 0})
    print(result)
    return result


@app.route("/api/updateWishes/", methods=["POST"])
def update_wishes(toupdate: toUpdate):
    database = getDatabase()
    coll = database["SberWishes"]
    coll.update_one({'sberuserid': toupdate.sberuserid}, {"$set": {'wishes': toupdate.list_of_wishes}}, upsert=True)
    return toupdate

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
