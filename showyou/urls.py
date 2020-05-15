#main 서브앱의 urls
#서브앱의 urls는 같은 위치의 view.py의 함수로 연결을 담당 (path)
#같은 위치의 views.py를 식별 못하면 import 

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('generic/',views.generic, name = 'generic'),
    path('elements/',views.elements, name = 'elements'),

    path('twitter/',views.twitter, name = 'twitter'),
    path('instagram/',views.instagram, name = 'instagram'),
    path('blog/',views.blog, name = 'blog'),

    path('twitter_user/',views.twitter_user, name = 'twitter_user'),
    path('instagram_user/',views.instagram_user, name = 'instagram_user'),
    path('blog_user/',views.blog_user, name = 'blog_user')
]
