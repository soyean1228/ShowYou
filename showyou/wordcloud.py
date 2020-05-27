import matplotlib
matplotlib.use('agg')
from collections import Counter
from wordcloud import WordCloud
from . import mongo_connection
import pymongo
import cv2
import math
from operator import itemgetter

        
def total_wordcloud():

    list = []

    for result in mongo_connection.textmining_result_find() :
       list.append(result["keyword"])
    
    result_list = []

    for i in list:
        result_list += i
    
   
    count = Counter(result_list)
    word  = dict(count.most_common())
    
    words = sorted(word.items(), key=itemgetter(1),reverse=True)
    
    wc = WordCloud(font_path='showyou/static/showyou/assets/fonts/MapoPeacefull.ttf', background_color='white', width=800, height=600, max_words= 50)
    cloud = wc.generate_from_frequencies(dict(words))

    wc.to_file('w_result1.png')
    imgfile = 'w_result1.png'
    img = cv2.imread(imgfile,1)
    cv2.imwrite('showYou/static/showyou/images/w.jpg',img)

total_wordcloud()