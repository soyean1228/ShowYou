from collections import Counter
from wordcloud import WordCloud
from . import mongo_connection
import pymongo
import cv2
import math
from operator import itemgetter
import random


def total_wordcloud(w_category):

    def this_color_func(word,font_size,position,orientation,random_state='No',**kwargs):
        if w_category == "IT":
            return "#0064CD"
        if w_category == "엔터테인먼트":
            return "#50D6FF"
        if w_category == "경제":
            return "#FF5675"
        if w_category == "건강":
            return "#aaaaaa"
        if w_category == "뷰티":
            return "#3CB371"
        if w_category == "기타":
            return "#7B68EE"

    category_list = []

    for result in mongo_connection.post_category_find():
        if result['category'] != w_category:
            category_list.append(result['post_id'])
        if w_category == '전체':
            print("전체로 나타낸다.")


    list = []
    if w_category == '전체':
        for result in mongo_connection.textmining_result_find() :
            list.append(result['keyword'])
    else:
        for result in mongo_connection.textmining_result_find() :
            if result['post_id'] not in category_list:
                list.append(result['keyword'])

    # print(list)

    result_list = []

    for i in list:
        result_list += i


    if len(result_list) == 0:
        result_list.append("해당하는 카테고리의 검색 결과가 없습니다.")

    count = Counter(result_list)
    word  = dict(count.most_common())

    words = sorted(word.items(), key=itemgetter(1),reverse=True)

    wc = WordCloud(font_path='showyou/static/showyou/assets/fonts/MapoPeacefull.ttf', background_color='white', width=800, height=600, max_words= 40, colormap = "summer")
    cloud = wc.generate_from_frequencies(dict(words))
    if w_category != "전체":
        wc.recolor(color_func=this_color_func,random_state=3)
    wc.to_file('w_result1.png')
    imgfile = 'w_result1.png'
    img = cv2.imread(imgfile,1)
    cv2.imwrite('ShowYou/static/showyou/images/w.jpg',img)

# total_wordcloud('경제')