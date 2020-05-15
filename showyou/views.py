from django.shortcuts import render
from django.http import HttpResponse
from . import twitter_parser
from . import textmining
from . import twitter_parser_personal
from . import twitter_parser_total
from . import blog_parser_total
from . import blog_parser_personal
# from . import keyword_wordcloud

def index(request):
    return render(request, 'showyou/index.html') 

def generic(request):
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

def instagram(request):
    search_keyword = request.GET.get('search_keyword', '')
    if search_keyword:
        print("있는 경우")
        print('search_keyword = ' + search_keyword)
        twitter_parser_total.parsing(search_keyword,'m')
        #textmining.analysis()
        return render(request, 'showyou/instagram.html')
    else :
        print("없는 경우")
        return render(request, 'showyou/instagram.html')
    
def instagram_user(request):
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