from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")

    return render(request, "accounts/register.html", {'form': form})