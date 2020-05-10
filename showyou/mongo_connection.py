HOSTNAME = "localhost"
PORT = 27017
import pymongo
 
client = pymongo.MongoClient(HOSTNAME, PORT)
db = client.ShowYou
collection = db.post
 
def save(post_id, person_id, post):
    collection.save({"post_id": post_id, "person_id": person_id "post": post})

