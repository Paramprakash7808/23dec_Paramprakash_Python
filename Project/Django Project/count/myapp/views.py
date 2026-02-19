from django.shortcuts import render

# Create your views here.
num = 0
def index(request):
    global num
    num += 1
    return render(request,'index.html',{'num':num})
