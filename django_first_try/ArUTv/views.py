from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def homepage(request):
    
    
    return render(request,'ArUTv/home.html')