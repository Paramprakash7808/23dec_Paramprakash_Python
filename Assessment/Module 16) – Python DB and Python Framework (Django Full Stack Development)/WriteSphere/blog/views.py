from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Post, Category, Comment, Like
from .forms import PostForm, CommentForm, PostFilterForm
from accounts.models import CustomUser


def home(request):
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags', 'likes')
    featured_posts = posts[:3]
    recent_posts = posts[3:9]
    categories = Category.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:6]
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]

    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'popular_posts': popular_posts,
    }
    return render(request, 'blog/home.html', context)


def post_list(request):
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    form = PostFilterForm(request.GET)

    if form.is_valid():
        author_q = form.cleaned_data.get('author')
        category_q = form.cleaned_data.get('category')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        search = form.cleaned_data.get('search')

        if author_q:
            posts = posts.filter(author__username__icontains=author_q)
        if category_q:
            posts = posts.filter(category=category_q)
        if date_from:
            posts = posts.filter(created_at__date__gte=date_from)
        if date_to:
            posts = posts.filter(created_at__date__lte=date_to)
        if search:
            posts = posts.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(author__username__icontains=search)
            )

    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'total_posts': posts.count(),
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    # Increment view count
    post.views += 1
    post.save(update_fields=['views'])

    comments = post.comments.filter(is_approved=True, parent=None).select_related('author').prefetch_related('replies__author')
    comment_form = CommentForm()
    is_liked = False

    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()

    # Related posts
    related_posts = Post.objects.filter(
        status='published', category=post.category
    ).exclude(pk=post.pk)[:3]

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect('accounts:login')
        comment_form = CommentForm(request.POST)
        parent_id = request.POST.get('parent_id')
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('blog:post_detail', slug=slug)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            # Save tags manually since we override save
            tags_input = form.cleaned_data.get('tags', '')
            tag_list = [t.strip() for t in tags_input.split(',') if t.strip()]
            post.tags.set(*tag_list)
            messages.success(request, f"Post '{post.title}' created successfully!")
            return redirect('blog:post_detail', slug=post.slug)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_admin_user():
        messages.error(request, "You are not allowed to edit this post.")
        return redirect('blog:post_detail', slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            tags_input = form.cleaned_data.get('tags', '')
            tag_list = [t.strip() for t in tags_input.split(',') if t.strip()]
            post.tags.set(*tag_list)
            messages.success(request, "Post updated successfully!")
            return redirect('blog:post_detail', slug=post.slug)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'post': post, 'action': 'Edit'})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_admin_user():
        messages.error(request, "You are not allowed to delete this post.")
        return redirect('blog:post_detail', slug=slug)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def like_toggle(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    like_obj, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like_obj.delete()
        is_liked = False
    else:
        is_liked = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_liked': is_liked,
            'like_count': post.get_like_count()
        })

    return redirect('blog:post_detail', slug=slug)


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user and not request.user.is_admin_user():
        messages.error(request, "You cannot edit this comment.")
        return redirect('blog:post_detail', slug=comment.post.slug)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated.")
            return redirect('blog:post_detail', slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_edit.html', {'form': form, 'comment': comment})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user and not request.user.is_admin_user():
        messages.error(request, "You cannot delete this comment.")
        return redirect('blog:post_detail', slug=comment.post.slug)

    slug = comment.post.slug
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted.")
    return redirect('blog:post_detail', slug=slug)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status='published', category=category).select_related('author')
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/category_posts.html', {
        'category': category, 'page_obj': page_obj
    })


def tag_posts(request, tag):
    posts = Post.objects.filter(status='published', tags__name__in=[tag]).select_related('author', 'category')
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/tag_posts.html', {'tag': tag, 'page_obj': page_obj})


@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    total_posts = user_posts.count()
    published_posts = user_posts.filter(status='published').count()
    draft_posts = user_posts.filter(status='draft').count()
    total_views = sum(p.views for p in user_posts)
    total_likes = sum(p.get_like_count() for p in user_posts)
    total_comments = sum(p.get_comment_count() for p in user_posts)

    context = {
        'user_posts': user_posts[:10],
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
    }
    return render(request, 'blog/dashboard.html', context)
