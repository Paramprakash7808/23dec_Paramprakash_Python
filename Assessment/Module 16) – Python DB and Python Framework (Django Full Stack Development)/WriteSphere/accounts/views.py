from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import CustomUser, Follow


def register_view(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to WriteSphere, {user.username}!")
            return redirect('blog:home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'blog:home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('blog:home')


@login_required
def profile_view(request, username=None):
    if username:
        profile_user = get_object_or_404(CustomUser, username=username)
    else:
        profile_user = request.user

    posts = profile_user.blog_posts.filter(status='published').order_by('-created_at')
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(
            follower=request.user, following=profile_user
        ).exists()

    followers = profile_user.followers.select_related('follower')
    following = profile_user.following.select_related('following')

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'followers': followers,
        'following': following,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    if target_user == request.user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Cannot follow yourself'}, status=400)
        messages.error(request, "You cannot follow yourself.")
        return redirect('accounts:profile_detail', username=username)

    follow_obj, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )
    if not created:
        follow_obj.delete()
        is_following = False
        msg = f"You unfollowed {target_user.username}."
    else:
        is_following = True
        msg = f"You are now following {target_user.username}."

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_following': is_following,
            'follower_count': target_user.get_follower_count(),
            'message': msg
        })

    messages.success(request, msg)
    return redirect('accounts:profile_detail', username=username)
