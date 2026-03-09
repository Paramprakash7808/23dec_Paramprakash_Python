from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        'placeholder': 'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Last Name'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        'placeholder': 'Password'
    }))
