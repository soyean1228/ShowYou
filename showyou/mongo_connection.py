import pymongo
import requests
from bs4 import BeautifulSoup
import datetime
import time
import GetOldTweets3 as got
from random import uniform
from tqdm import tqdm
import pandas as pd
from . import twitterParser
 
def save(post_id, person_id, content):
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

    # collection.insert_one({"post_id": 3, "person_id": 3, "post": "third"})
    
    collection.insert_one({"post_id": post_id, "person_id": person_id, "post": content})
    
    # results = collection.find()
    # for result in results :
    #     print(result)

