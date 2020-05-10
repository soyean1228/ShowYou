from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    return render(request, 'main/index.html') 

def generic(request):
    return render(request, 'main/generic.html') 

def elements(request):
    return render(request, 'main/elements.html') 