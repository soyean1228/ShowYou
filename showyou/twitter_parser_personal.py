import time
from random import uniform
from tqdm import tqdm_notebook
from bs4 import BeautifulSoup
import GetOldTweets3 as got
from random import uniform
from tqdm import tqdm
import pandas as pd

import pymongo
from . import mongo_connection

def parsing(id):

    # 트윗 수집 기준 정의
    tweetCriteria = got.manager.TweetCriteria().setUsername(id).setMaxTweets(20)
    
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)

    # initialize
    tweet_list = []
    
    i = 0
    for index in tqdm(tweet):
        # 메타데이터 목록 
        username = index.username
        content = index.text
        # 결과 합치기
        info_list = {}
        info_list['post_id'] = i
        info_list['person_id'] = username
        info_list['post'] = content
        tweet_list += [info_list]
        i = i + 1

    mongo_connection.post_insert(tweet_list)

    
    twitter_df = pd.DataFrame( tweet_list, columns = [ "user_name", "text"])

    # csv 파일 만들기
    twitter_df.to_csv("{}_twitter_person.csv".format(id))
    print("=== {} tweets are successfully saved ===".format(len(tweet_list)))
