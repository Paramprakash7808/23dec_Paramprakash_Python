from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
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
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('profile', username=username)

# ── Admin User Management ───────────────────────────────────────────────────

@login_required
def user_management(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('post_list')
    
    query = request.GET.get('q', '')
    users = User.objects.all().order_by('-date_joined')
    
    if query:
        users = users.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
        
    context = {
        'users_list': users,
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'blocked_users': User.objects.filter(is_active=False).count(),
        'search_query': query
    }
    return render(request, 'users/user_management.html', context)

@login_required
def toggle_user_status(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('post_list')
        
    user_to_toggle = get_object_or_404(User, id=user_id)
    if user_to_toggle.is_superuser:
        messages.error(request, 'Cannot block/unblock a superuser.')
    else:
        user_to_toggle.is_active = not user_to_toggle.is_active
        user_to_toggle.save()
        status = "unblocked" if user_to_toggle.is_active else "blocked"
        messages.success(request, f'User {user_to_toggle.username} has been {status}.')
        
    return redirect('user_management')
