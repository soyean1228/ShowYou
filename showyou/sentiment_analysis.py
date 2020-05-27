import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pymongo
import cv2
from matplotlib import font_manager,rc
from . import mongo_connection


#한글 font 설정
font = matplotlib.font_manager.FontProperties(fname="showyou/static/showyou/assets/fonts/MapoPeacefull.ttf")

#Thread처리
plt.switch_backend('agg')


def search(name, people):
    return [element for element in people if element['keyword'] == name]
#리스트 전부 가져오기
def Sentiment_Analysis():

    sentiment_list = mongo_connection.sentiment_analysis_result_find()
    textmining_list = mongo_connection.textmining_result_find()


    #post_id /긍정(+1),부정(-1),중립(0) 받아오기
    sentiment_data =[]
    for i in sentiment_list:
        sentiment_data.append(i['sentiment'])

    # post_id / keyword받아오기
    keyword_list =[]
    post_id = []
    for i in textmining_list:
        post_id.append(i['post_id'])
        keyword_list.append(i['keyword'])

    for i in post_id:
       print(i, '/', keyword_list[i], '/', sentiment_data[i])


    #합친 딕션너리
    post_id_to_keywords = dict(zip(post_id,keyword_list))
    post_id_to_sentiment = dict(zip(post_id,sentiment_data))
    print(post_id_to_keywords)
    print(post_id_to_sentiment)


    #키워드에 따른 빈도수 구하기
    keywords = [] #모든 키워드들의 집합
    count={} #{키워드: 빈도}의 순서쌍
    positive={}#{키워드: 긍정의 빈도}의 순서쌍
    neutral = {} #{키워드: 중립의 빈도}의 순서쌍
    negative = {}#{키워드: 부정의 빈도}의 순서쌍

    for post_id in post_id:
        for keyword in post_id_to_keywords[post_id]:
            if(keyword not in keywords):
                keywords.append(keyword)
                count[keyword] = 0
                negative[keyword] = 0
                neutral[keyword] = 0
                positive[keyword] = 0

            count[keyword] += 1
            senti = post_id_to_sentiment[post_id]

            if(senti == 1):
                positive[keyword] += 1
            elif(senti == 0):
                neutral[keyword] += 1
            else:
                negative[keyword] += 1

    sentiment = {}

    for k in list(keywords):
        if(positive[k] > negative[k] and positive[k]>neutral[k]):
            sentiment[k] = 1
        elif(negative[k]>positive[k] and negative[k]>neutral[k]):
            sentiment[k] = -1
        else:
            sentiment[k] = 0


    print('keywords')
    print(keywords)
    print('count')
    print(count)
    print('sentiment')
    print(sentiment)


    input_keywords = []
    input_count = []
    for key,value in count.items():
        if(value > 3):  #원의 갯수 여기를 바꿔주기
            input_keywords.append(key)
            input_count.append(value)

    input_sentiment = []
    for keyword in input_keywords:
        for key,value in sentiment.items():
            if(keyword == key):
                input_sentiment.append(value)

    print(input_keywords)
    print(input_count)
    print(input_sentiment)

    #원그래프 만들기
    r = list(input_count)

    class C():
        def __init__(self,r):
            self.N = len(r)
            self.x = np.ones((self.N,3))
            self.x[:,2] = r
            maxstep = 2*self.x[:,2].max()
            length = np.ceil(np.sqrt(self.N))
            grid = np.arange(0,length*maxstep,maxstep)
            gx,gy = np.meshgrid(grid,grid)
            self.x[:,0] = gx.flatten()[:self.N]
            self.x[:,1] = gy.flatten()[:self.N]
            self.x[:,:2] = self.x[:,:2] - np.mean(self.x[:,:2], axis=0)

            self.step = self.x[:,2].min()
            self.p = lambda x,y: np.sum((x**2+y**2)**2)
            self.E = self.energy()
            self.iter = 1.

        def minimize(self):
            while self.iter < 1000*self.N:
                for i in range(self.N):
                    rand = np.random.randn(2)*self.step/self.iter
                    self.x[i,:2] += rand
                    e = self.energy()
                    if (e < self.E and self.isvalid(i)):
                        self.E = e
                        self.iter = 1.
                    else:
                        self.x[i,:2] -= rand
                        self.iter += 1.

        def energy(self):
            return self.p(self.x[:,0], self.x[:,1])

        def distance(self,x1,x2):
            return np.sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)-x1[2]-x2[2]

        def isvalid(self, i):
            for j in range(self.N):
                if i!=j:
                    if self.distance(self.x[i,:], self.x[j,:]) < 0:
                        return False
            return True

        def plot(self, ax):
            index=0
            for i in range(self.N):
                keyword=input_keywords[index]
                #if(input_sentiment[keyword]==1):
                if(input_sentiment[index]==1):
                    color='#6796DC'
                #elif(input_sentiment[keyword]==0):
                elif(input_sentiment[index]==0):
                    color= '#97CA73'
                else:
                    color='#E97A7A'

                circ = plt.Circle(self.x[i,:2],self.x[i,2], color = color)
                ax.add_patch(circ)
                ax.annotate(keyword, xy=(self.x[i,:2]), fontsize=10, ha="center",FontProperties = font)
                index += 1

    c = C(r)

    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    ax.axis("off")

    c.minimize()
    c.plot(ax)
    ax.relim()
    ax.autoscale_view()

     #그림 저장
    plt.savefig('s_result.png')

    #그래프 그려주기
    imgfile = 's_result.png'
    img = cv2.imread(imgfile,1)
    cv2.imwrite('showyou/static/showyou/images/senti.jpg',img)

    #그래프 띄우기
    #plt.show()