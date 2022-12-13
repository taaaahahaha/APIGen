import pymongo
from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://taaham:123@cluster0.imuxc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["testing-techfest"]
collection = db["collection1"]

def insert_one():
    x = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"]}
    collection.insert_one(x)

def insert_many():
    x = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"]}
    y = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"]}
    collection.insert_many([x,y])

def find():
    results = collection.find({"author":"Mike"})
    # results = collection.find_one({"author":"Mike"})

    for res in results:
        print(res)
        
def find_all():
    results = collection.find({}) 

    for res in results:
        print(res)
        

def delete_one():
    x = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"]}
    collection.delete_one(x)

    # collection.delete_many({})


def update():
    collection.update_one({"author": "Mike"},{"$set":{"author":"Mike2"}})  # You can add a new field as well


def count():
    print(collection.count_documents({}))
    

count()
find_all()
print("DONE")