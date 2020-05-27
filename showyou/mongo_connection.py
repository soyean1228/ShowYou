import pymongo
import requests
from bs4 import BeautifulSoup
import datetime
import time
import GetOldTweets3 as got
from random import uniform
from tqdm import tqdm
import pandas as pd

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

def sentiment_analysis_result_find():
    client = pymongo.MongoClient(
        "mongodb+srv://showyou:showyou@showyou-aznp8.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client.get_database('ShowYou')
    collection = db.get_collection('sentiment_analysis_result')
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
    # doc = collection.find()
    # for result in doc :
    #     print(result)
    client.close()

def textmining_result_find():
    client = pymongo.MongoClient(
        "mongodb+srv://showyou:showyou@showyou-aznp8.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client.get_database('ShowYou')
    collection = db.get_collection('textmining_result')
    doc = collection.find()
    # for result in doc :
    #     print(result)
    client.close()
    return doc
