
import pymongo
 
client = pymongo.MongoClient(
        "mongodb+srv://showyou:showyou@showyou-aznp8.mongodb.net/test?retryWrites=true&w=majority"
    )
# db = client.ShowYou
# collection = db.post
# collection.insertOne({"post_id": 1, "person_id": 1, "post": "ddd"})
 
db = client.get_database('ShowYou')
collection = db.get_collection('post')
# collection_list = db.collection_names()
# print(collection_list)

collection.insert_one({"post_id": 3, "person_id": 3, "post": "third"})

results = collection.find()
for result in results :
    print(result)


# collection.insert({"post_id": 1})

def save(post_id, person_id, post):
    collection.save({"post_id": post_id, "person_id": person_id, "post": post})

