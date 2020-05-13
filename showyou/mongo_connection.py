import pymongo
import requests
from bs4 import BeautifulSoup
import datetime
import time
import GetOldTweets3 as got
from random import uniform
from tqdm import tqdm
import pandas as pd
from . import twitter_parser
 
# def save(post_id, person_id, content):
#     client = pymongo.MongoClient(
#         "mongodb+srv://showyou:showyou@showyou-aznp8.mongodb.net/test?retryWrites=true&w=majority"
#     )
#     db = client.get_database('ShowYou')
#     collection = db.get_collection('post')
#     collection.insert_one({"post_id": post_id, "person_id": person_id, "post": content})
    
#     # results = collection.find()
#     # for result in results :
#     #     print(result)

def post_insert(list):
    client = pymongo.MongoClient(
        "mongodb+srv://showyou:showyou@showyou-aznp8.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client.get_database('ShowYou')
    collection = db.get_collection('post')
    collection.drop() 
    collection.insert(list)
    # results = collection.find()
    # for result in results :
    #     print(result)
    client.close()

def post_find():
    client = pymongo.MongoClient(
        "mongodb+srv://showyou:showyou@showyou-aznp8.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client.get_database('ShowYou')
    collection = db.get_collection('post')
    doc = collection.find()
    # for result in doc :
    #     print(result)
    client.close()
    return doc

def textmining_result_insert(list):
    client = pymongo.MongoClient(
        "mongodb+srv://showyou:showyou@showyou-aznp8.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client.get_database('ShowYou')
    collection = db.get_collection('textmining_result')
    collection.drop() 
    collection.insert(list)
    doc = collection.find()
    for result in doc :
        print(result)
    client.close()

