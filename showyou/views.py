from django.shortcuts import render
from django.http import HttpResponse
from . import twitter_parser
from . import textmining
from . import twitter_parser_personal
from . import twitter_parser_total
from . import blog_parser_total
from . import blog_parser_personal
from . import instagram_parser_personal
from . import sentiment_analysis
from . import mongo_connection
from . import keyword_wordcloud
# 
import json
import numpy as np
from django.http import JsonResponse

def index(request):
    # sentiment_analysis.Sentiment_Analysis()
    keyword_wordcloud.total_wordcloud()
    return render(request, 'showyou/index.html') 

# 
# def data(request):     
#     x = np.array(['2017-07-10', '2017-07-11', '2017-07-12', '2017-07-13', '2017-07-14'])
#     # post_list = mongo_connection.post_id_find()
#     # x = np.array(post_list)
#     y = np.array([58.13, 53.98, 67.00, 89.70, 99.00])
#     # myData = json.dumps([{"date": str(x[i]), "close": y[i]} for i in range(5)])
#     myData = json.dumps([{"date": x[i] , "close": y[i]} for i in range(5)])
#     return JsonResponse(myData, safe=False)

# def sentiment(request):
#     return render(request, 'showyou/sentiment_result.html', context=None)


def generic(request):
    # keyword_wordcloud.total_wordcloud()
    return render(request, 'showyou/generic.html') 

def elements(request):
    return render(request, 'showyou/elements.html') 

def twitter(request):
    search_keyword = request.GET.get('search_keyword', '')
    if search_keyword:
        print("있는 경우")
        print('search_keyword = ' + search_keyword)
        twitter_parser_total.parsing(search_keyword,'m')
        textmining.analysis()
        # keyword_wordcloud.show()
        return render(request, 'showyou/twitter_result.html')
    else :
        print("없는 경우")
        return render(request, 'showyou/twitter.html') 

def twitter_user(request):
    search_keyword = request.GET.get('search_keyword', '')
    if search_keyword:
        print("있는 경우")
        print('search_keyword = ' + search_keyword)
        twitter_parser_total.parsing(search_keyword,'m')
        textmining.analysis()
        return render(request, 'showyou/twitter.html')
    else :
        print("없는 경우")
        return render(request, 'showyou/twitter.html') 

def blog(request):
    print("blog 크롤링")
    search_keyword = request.GET.get('search_keyword', '')
    print('search_keyword = ' + search_keyword)
    if search_keyword:
        print("있는 경우")
        blog_parser_total.parsing(search_keyword,'m')
        # blog_parser_personal.parsing(search_keyword)
        textmining.analysis()
        return render(request, 'showyou/blog.html') 
    else :
        print("없는 경우")
        return render(request, 'showyou/blog.html') 

def blog_user(request):
    print("blog 크롤링")
    search_keyword = request.GET.get('search_keyword', '')
    print('search_keyword = ' + search_keyword)
    if search_keyword:
        print("있는 경우")
        blog_parser_total.parsing(search_keyword,'m')
        # blog_parser_personal.parsing(search_keyword)
        textmining.analysis()
        return render(request, 'showyou/blog.html') 
    else :
        print("없는 경우")
        return render(request, 'showyou/blog.html') 

def instagram_user(request):
    print("instagram 크롤링")
    search_keyword = request.GET.get('search_keyword', '')
    print('search_keyword = ' + search_keyword)
    if search_keyword:
        print("있는 경우")
        instagram_parser_personal.parsing(search_keyword)
        textmining.analysis()
        return render(request, 'showyou/instagram_user.html')
    else :
        print("없는 경우")   
        return render(request, 'showyou/instagram_user.html')
    
def instagram(request):
    search_keyword = request.GET.get('search_keyword', '')
    if search_keyword:
        print("있는 경우")
        print('search_keyword = ' + search_keyword)
        twitter_parser_total.parsing(search_keyword,'m')
        #textmining.analysis()
        return render(request, 'showyou/instagram_user.html')
    else :
        print("없는 경우")
        return render(request, 'showyou/instagram_user.html')