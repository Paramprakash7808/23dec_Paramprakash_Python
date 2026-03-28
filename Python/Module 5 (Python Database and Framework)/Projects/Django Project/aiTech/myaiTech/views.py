from django.shortcuts import render
from .forms import *

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == 'POST':
        form = studform(request.POST)
        if form.is_valid():
            form.save()
            print("Data Inserted!")
        else:
            print(form.errors)
    return render(request,'contact.html')

def project(request):
    return render(request,'project.html')

def service(request):
    return render(request,'service.html')