import pymongo
from bson.json_util import dumps
from pymongo import MongoClient
from api_key import mongoDBaccess
from datetime import datetime, timedelta
cluster = MongoClient(mongoDBaccess)


# db and collection are the parameters used to get to desired section of database
# posts are the new items you are adding to the database
# Duplicate _id items fail to add
def addManyPost(db, collection, posts):
    database = cluster[db]
    coll = database[collection]
    try:
        result = coll.insert_many(posts, ordered=False)
        print("Posts created.")
    except pymongo.errors.BulkWriteError as e:
        print(e.details['writeErrors'][0]['errmsg'])




# Try except borrowed:
# https://stackoverflow.com/questions/44838280/how-to-ignore-duplicate-key-errors-safely-using-insert-many

# db and collection are the parameters used to get to desired section of database
# post is the new item you are adding to the database
# Duplicate _id items fail to add
def addPost(db, collection, post):
    database = cluster[db]
    coll = database[collection]
    try:
        coll.insert_one(post)
        return "success"
    except pymongo.errors.DuplicateKeyError as e:
        return "Duplicate Key"
    except:
        return "fail"



# db and collection are the parameters used to get to desired section of database
# parameter and value filter which posts you will be deleting
def deleteManyPost(db, collection, parameter, value):
    database = cluster[db]
    coll = database[collection]
    try:
        coll.delete_many({parameter: value})
        print("Posts deleted.")
    except:
        print("Deletion failed.")


# Example:
# deleteManyPost("Inventory", "Books", "rec_grade", "Middle")


# db and collection are the parameters used to get to desired section of database
# parameter and value filter which post you will be deleting
def deletePost(db, collection, parameter, value):
    database = cluster[db]
    coll = database[collection]
    try:
        coll.delete_one({parameter: value})
        print("Post deleted.")
    except:
        print("Deletion failed.")


# Example:
# deletePost("Inventory", "Books", "_id","978-0590353427")


# db and collection are the parameters used to get to desired section of database
# parameter and value filter which posts you are searching for
# Returns empty vector if no results are found
def findManyPost(db, collection, parameter, value):
    database = cluster[db]
    coll = database[collection]
    try:
        # case to return all data
        if parameter == "" or value == "":
            results = coll.find({})
        else:
            results = coll.find({parameter: value})
        print("Search success.")
        data = []
        for result in results:
            data.append(result)
        return data
    except:
        print("Search failed.")


# Example:
# print(findManyPost("Inventory", "Books", "genre", "Fanasy"))


# db and collection are the parameters used to get to desired section of database
# parameter and value filter which post you are trying to find
# Duplicate _id items fail to add
def findPost(db, collection, parameter, value):
    database = cluster[db]
    coll = database[collection]
    try:
        results = coll.find_one({parameter: value})
        return results
    except:
        return "fail"


# Example:
# data = findPost("Userdata", "Users","_id","jimmylynch")
# for items in data:
#     if items == "password":
#         print(passwordDecrypt(data[items]))
#     else:
#         print(data[items])


# db and collection are the parameters used to get to desired section of database
# search_parameter and search_value filter which posts you will be updating
# new_parameter and new_value are what you are updating
def updateManyPost(db, collection, search_parameter, search_value, new_parameter, new_value):
    database = cluster[db]
    coll = database[collection]
    try:
        result = coll.update_many({search_parameter: search_value}, {"$set": {new_parameter: new_value}})
        print("Posts updated.")
    except:
        print("Update failed.")


# Example:
# updateManyPost("Inventory","Books","genre", "Fantasy","available", True)


# db and collection are the parameters used to get to desired section of database
# search_parameter and search_value filter which post you will be updating
# new_parameter and new_value are what you are updating
# if there are multiple posts that match the search, only the first post found will update
def updatePost(db, collection, search_parameter, search_value, new_parameter, new_value):
    database = cluster[db]
    coll = database[collection]
    try:
        coll.update_one({search_parameter: search_value}, {"$set": {new_parameter: new_value}})
        print("Post updated.")
    except:
        print("Update failed.")

