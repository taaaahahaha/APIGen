import pymongo
from pymongo import MongoClient

# cluster = MongoClient("mongodb+srv://taaham:123@cluster0.imuxc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = cluster["testing-techfest"]
# collection = db["collection1"]

def connect(url,database):
    cluster = MongoClient(url)
    db = cluster[database]
    # collection = db[collection]
    return db

def insert_one(db, collection):
    x = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"]}
    collection.insert_one(x)

def insert_many(db, collection,data):
    # x = {"author": "Mike",
    #         "text": "My first blog post!",
    #         "tags": ["mongodb", "python", "pymongo"]}
    # y = {"author": "Mike",
    #         "text": "My first blog post!",
    #         "tags": ["mongodb", "python", "pymongo"]}
    # collection.insert_many([x,y])
    try:
        col = db[collection]
        results = col.insert_many(data)
        return True, results
    except Exception as e:
        print(e)
        return False, e

def find(db, collection,query):
    try:
        col = db[collection]
        results = col.find(query)
        # results = col.find({"author":"Mike"})
        # results = collection.find_one({"author":"Mike"})

        # for res in results:
        #     print(res)
        return True, results
    except Exception as e:
        print(e)
        return False, e
        
        
def find_all(db, collection):
    try:
        col = db[collection]
        results = col.find({}) 
        # for res in results:
        #     print(res)
        return True, results
    except Exception as e:
        print(e)
        return False, e

    
        

def delete(db, collection,query):
    # x = {"author": "Mike",
    #         "text": "My first blog post!",
    #         "tags": ["mongodb", "python", "pymongo"]}
    # collection.delete_one(x)
    # collection.delete_many({})
    try:
        col = db[collection]
        results = col.delete_many(query) 
        # for res in results:
        #     print(res)
        return True, results
    except Exception as e:
        print(e)
        return False, e


def update(db, collection,data,filters):
    # collection.update_one({"author": "Mike"},{"$set":{"author":"Mike2"}})  # You can add a new field as well
    # collection.update_many({"author": "Mike"},{"$set":{"author":"Mike2"}})  # You can add a new field as well
    try:
        col = db[collection]
        results = col.update_many(filters,{"$set":data}) 
        # for res in results:
        #     print(res)
        return True, results
    except Exception as e:
        print(e)
        return False, e

def count(db, collection):
    print(collection.count_documents({}))
    

# count()
# find_all()
# print("DONE")