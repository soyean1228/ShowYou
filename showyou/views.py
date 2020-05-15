from django.shortcuts import render
from django.http import HttpResponse
from . import twitter_parser
from . import textmining
from . import twitter_parser_personal
from . import twitter_parser_total
from . import blog_parser_total
from . import blog_parser_personal

def index(request):
    return render(request, 'showyou/index.html') 

def generic(request):
    return render(request, 'showyou/generic.html') 

def elements(request):
    return render(request, 'showyou/elements.html') 

def twitterSelect(request):
    search_keyword = request.GET.get('search_keyword', '')
    print('search_keyword = ' + search_keyword)
    if search_keyword:
        print("있는 경우")
        # twitter_parser.parsing(search_keyword)
        twitter_parser_personal.parsing(search_keyword)
        # blog_parser_personal.parsing(search_keyword)
        # blog_parser_total.parsing(search_keyword,'m')
        textmining.analysis()
        return render(request, 'showyou/twitterSelect.html') 
    else :
        print("없는 경우")
        return render(request, 'showyou/twitterSelect.html') 

def blogSelect(request):
    search_keyword = request.GET.get('search_keyword', '')
    print('search_keyword = ' + search_keyword)
    if search_keyword:
        print("있는 경우")
        # blog_parser_total.parsing(search_keyword,'m')
        blog_parser_personal.parsing(search_keyword)
        textmining.analysis()
        return render(request, 'showyou/twitterSelect.html') 
    else :
        print("없는 경우")
        return render(request, 'showyou/twitterSelect.html') 
