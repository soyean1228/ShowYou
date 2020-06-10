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

def sentiment_to_color(sentiment):
    hue_for_positive=215.9
    saturation_for_positive=53.2
    value_for_positive=86.3

    hue_for_negative=0
    saturation_for_negative=47.6
    value_for_negative=91.4

    if sentiment<1/2:
        positive=((((2-0)*(sentiment-0))**2)/(2-0))+0

    else:
        positive=((((2-0)*(sentiment-(1/2)))**(1/2))/(2-0))+(1/2)
    #positive=sentiment

    negative=1-sentiment

    hue=positive*hue_for_positive+negative*hue_for_negative
    saturation=positive*saturation_for_positive+negative*saturation_for_negative
    value=positive*value_for_positive+negative*value_for_negative

    import matplotlib
    RGB=matplotlib.colors.hsv_to_rgb([hue/360,saturation/100,value/100])
    color=matplotlib.colors.to_hex(RGB,keep_alpha=False)

    return(color)


##


def visualize(category):
    print('sentiment visualization: under visualization.')


    keywords={}
    sentiment={}

    for row in mongo_connection.textmining_result_find():
        keywords[row['post_id']]=row['keyword']

    for row in mongo_connection.sentiment_analysis_result_find():
        sentiment[row['post_id']]=row['sentiment']


    count={}#{키워드: 빈도}의 순서쌍
    accumulated_sentiment={}#{키워드: 빈도*감성}의 순서쌍

    for row in mongo_connection.post_category_find():
        if category=='전체' or row['category']==category:
            post_id=row['post_id']

            for keyword in keywords[post_id]:
                if keyword not in count.keys():
                    count[keyword]=0
                    accumulated_sentiment[keyword]=0

                count[keyword]+=1
                accumulated_sentiment[keyword]+=sentiment[post_id]


    sentiment={}

    for keyword in count.keys():
        sentiment[keyword]=accumulated_sentiment[keyword]/count[keyword]


    count=dict(sorted(count.items(), key=lambda key: key[1],reverse=True)[0:10])
    counts=list(count.values())
    keywords=list(count.keys())


    for keyword in keywords:
        print('keyword:',keyword,'\t\tcount:',count[keyword],'\t\tsentiment:',sentiment[keyword])
    print()


    ##


    if len(counts)>0:
        import numpy as np
        import matplotlib.pyplot as plt

        # create 10 circles with different radii
        #r = np.random.randint(5,15, size=10)
        r = list(counts)

        class C():
            def __init__(self,r):
                self.N = len(r)
                self.x = np.ones((self.N,3))
                self.x[:,2] = counts
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

                    keyword=keywords[index]

                    circ = plt.Circle(self.x[i,:2],self.x[i,2], color = sentiment_to_color(sentiment[keyword]))
                    ax.add_patch(circ)

                    size=19*((counts[index]/(sum(counts)/len(counts)))/(((len(keyword)/2)**2+1**2)**1/2))
                    #size=19*((counts[index]/(sum(counts)/len(counts)))/((((len(keyword)/2)/2)**2+1**2)**1/2))
                    font = matplotlib.font_manager.FontProperties(fname='/home/showyou/ShowYou/showyou/static/showyou/assets/fonts/MapoPeacefull.ttf', size=size)
                    ax.annotate(keyword, xy=self.x[i,:2], ha="center", color='white', FontProperties = font)
                    print(self.x[i,:2])

                    index += 1

        c = C(r)

        fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
        ax.axis("off")

        c.minimize()

        c.plot(ax)
        ax.relim()
        ax.autoscale_view()


    ##
        plt.savefig('s_result.png')
        image=cv2.imread('s_result.png',1)

    else:
        image=cv2.imread('sentiment visualization error.png',1)

    cv2.imwrite('showYou/static/showyou/images/senti.jpg',img)


    print('sentiment visualization: visualized sentiments.')
    print()
