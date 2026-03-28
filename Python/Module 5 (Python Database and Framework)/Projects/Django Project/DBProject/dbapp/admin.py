from django.contrib import admin
from .models import *

# Register your models here.

class studata(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['name','email','mobile','dob']

admin.site.register(studinfo,studata)