from django import forms
from .models import *

class SignupForm(forms.ModelForm):
    class Meta:
        model = usersignup
        fields = '__all__'