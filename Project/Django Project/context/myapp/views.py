from django.shortcuts import render
import random

# Create your views here.
def index(request):
    num = random.randint(1,1000)
    name = 'Prakash'
    return render(request,'index.html',{'name':name,'num':num})
