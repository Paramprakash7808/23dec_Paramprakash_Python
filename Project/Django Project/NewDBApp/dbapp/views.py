from django.shortcuts import render
from .forms import *

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = studform(request.POST)
        if form.is_valid():
            form.save()
            print('Data Inserted!')
        else:
            print(form.errors)
    return render(request,'index.html')