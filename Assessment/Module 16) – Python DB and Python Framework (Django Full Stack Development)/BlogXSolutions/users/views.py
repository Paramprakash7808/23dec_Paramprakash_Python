from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from .models import Profile, Follow


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Default to Author role for assessment purposes
            author_group, created = Group.objects.get_or_create(name='Author')
            user.groups.add(author_group)
            
            messages.success(request, f'Account created for {user.username}! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, followed=user_obj).exists()
    
    context = {
        'profile_user': user_obj,
        'is_following': is_following,
        'posts': user_obj.posts.all().order_by('-created_at')
    }
    return render(request, 'users/profile.html', context)

@login_required
def toggle_follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        follow_obj, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        if not created:
            follow_obj.delete()
    return redirect('profile', username=username)
