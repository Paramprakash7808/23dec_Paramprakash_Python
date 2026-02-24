from django.shortcuts import render,redirect
from .forms import *

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = studform(request.POST)
        if form.is_valid():
            form.save()
            print("Data Inserted!")
        else:
            print(form.errors)
    return render(request,'index.html')

def displaydata(request):
    stdata = studinfo.objects.all()
    return render(request,'displaydata.html',{'stdata':stdata})

def update(request,id):
    stid = studinfo.objects.get(id=id)
    if request.method == 'POST':
        form = studform(request.POST,instance=stid)
        if form.is_valid():
            form.save()
            print("Data Updated!")
            return redirect('displaydata')
        else:
            print(form.errors)
    return render(request,'update.html',{'stid':stid})

def deletedata(request,id):
    stid = studinfo.objects.get(id=id)
    studinfo.delete(stid)
    return redirect('displaydata')