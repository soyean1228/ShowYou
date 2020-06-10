from django.shortcuts import render
from django.http import HttpResponse
from . import twitter_parser
from . import textmining
from . import twitter_parser_personal
from . import twitter_parser_total
from . import blog_parser_total
from . import blog_parser_personal
from . import instagram_parser_personal
from . import instagram_parser_total
from . import sentiment_visualization
from . import wordcloud
from . import Analyzer

def index(request):
    return render(request, 'showyou/index.html')

def generic(request):
    return render(request, 'showyou/generic.html')

def elements(request):
    return render(request, 'showyou/elements.html')

def twitter(request):
    search_keyword = request.GET.get('search_keyword', '')
    date = request.GET.get('date')
    print(date)
    if search_keyword:
        print("있는 경우")
        print(date)
        print('search_keyword = ' + search_keyword)
        twitter_parser_total.parsing(search_keyword,date)
        textmining.analysis()
        Analyzer.analyze()
        wordcloud.total_wordcloud('전체')
        sentiment_visualization.visualize('전체')
        return render(request, 'showyou/visualization.html', {'keyword': search_keyword, 'date': date})
    else :
        print("없는 경우")
        return render(request, 'showyou/twitter.html')

def twitter_user(request):
    search_keyword = request.GET.get('search_keyword', '')
    date = request.GET.get('date')
    print(date)
    if search_keyword:
        print("있는 경우")
        print('search_keyword = ' + search_keyword)
        twitter_parser_personal.parsing(search_keyword)
        textmining.analysis()
        Analyzer.analyze()
        wordcloud.total_wordcloud('전체')
        sentiment_visualization.visualize('전체')
        return render(request, 'showyou/visualization.html', {'keyword': search_keyword, 'date': date})
    else :
        print("없는 경우")
        return render(request, 'showyou/twitter_user.html')

def blog(request):
    print("blog 크롤링")
    search_keyword = request.GET.get('search_keyword', '')
    date = request.GET.get('date')
    print(date)
    print('search_keyword = ' + search_keyword)
    if search_keyword:
        print("있는 경우")
        blog_parser_total.parsing(search_keyword,date)
        textmining.analysis()
        Analyzer.analyze()
        sentiment_visualization.visualize('전체')
        wordcloud.total_wordcloud('전체')
        return render(request, 'showyou/visualization.html', {'keyword': search_keyword, 'date': date})
    else :
        print("없는 경우")
        return render(request, 'showyou/blog.html')

def blog_user(request):
    print("blog 크롤링")
    search_keyword = request.GET.get('search_keyword', '')
    date = request.GET.get('date')
    print(date)
    print('search_keyword = ' + search_keyword)
    if search_keyword:
        print("있는 경우")
        blog_parser_total.parsing(search_keyword,date)
        textmining.analysis()
        Analyzer.analyze()
        wordcloud.total_wordcloud('전체')
        sentiment_visualization.visualize('전체')
        return render(request, 'showyou/visualization.html', {'keyword': search_keyword, 'date': date})
    else :
        print("없는 경우")
        return render(request, 'showyou/blog_user.html')

def instagram(request):
    search_keyword = request.GET.get('search_keyword', '')
    if search_keyword:
        print("있는 경우")
        print('search_keyword = ' + search_keyword)
        instagram_parser_total.parsing(search_keyword)
        textmining.analysis()
        Analyzer.analyze()
        wordcloud.total_wordcloud('전체')
        sentiment_visualization.visualize('전체')
        return render(request, 'showyou/visualization.html', {'keyword': search_keyword, 'date': 0 })
    else :
        print("없는 경우")
        return render(request, 'showyou/instagram.html')

def instagram_user(request):
    search_keyword = request.GET.get('search_keyword', '')
    if search_keyword:
        print("있는 경우")
        print('search_keyword = ' + search_keyword)
        instagram_parser_personal.parsing(search_keyword)
        textmining.analysis()
        Analyzer.analyze()
        wordcloud.total_wordcloud('전체')
        sentiment_visualization.visualize('전체')
        return render(request, 'showyou/visualization.html', {'keyword': search_keyword, 'date': 0})
    else :
        print("없는 경우")
        return render(request, 'showyou/instagram_user.html')

def visualization(request, search_keyword, date, category):
    print(category)
    wordcloud.total_wordcloud(category)
    sentiment_visualization.visualize(category)
    return render(request, 'showyou/visualization.html', {'keyword': search_keyword, 'date': date})


