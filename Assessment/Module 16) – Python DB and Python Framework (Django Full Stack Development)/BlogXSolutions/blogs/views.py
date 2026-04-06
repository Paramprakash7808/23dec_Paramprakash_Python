from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment, Like
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class PostListView(ListView):
    model = Post
    template_name = 'blogs/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtering logic
        author = self.request.GET.get('author')
        category = self.request.GET.get('category')
        q = self.request.GET.get('q')

        if author:
            queryset = queryset.filter(author__username=author)
        if category:
            queryset = queryset.filter(category__slug=category)
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(content__icontains=q)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        user = self.request.user
        context['comments'] = post.comments.order_by('-created_at')
        context['is_liked'] = user.is_authenticated and post.likes.filter(user=user).exists()
        
        if user.is_authenticated:
            from users.models import Follow
            context['is_following_author'] = Follow.objects.filter(follower=user, followed=post.author).exists()
        else:
            context['is_following_author'] = False
            
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blogs/post_form.html'
    fields = ['title', 'category', 'cover_image', 'content', 'tags']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not Category.objects.exists():
            messages.warning(
                request,
                '⚠️ No categories exist yet. Please create a category before writing a post.'
            )
            return redirect('category_manage')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if not form.cleaned_data.get('category'):
            form.add_error('category', 'A category is required to publish a post.')
            return self.form_invalid(form)
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blogs/post_form.html'
    fields = ['title', 'category', 'cover_image', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blogs/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_obj, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like_obj.delete()
        
    return redirect('post_detail', slug=slug)

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect('post_detail', slug=slug)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.user or request.user == comment.post.author:
        post_slug = comment.post.slug
        comment.delete()
        return redirect('post_detail', slug=post_slug)
    return redirect('post_list')

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        return redirect('post_list')
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.save()
    return redirect('post_detail', slug=comment.post.slug)


# ── Category Management ─────────────────────────────────────────────────────

@login_required
def category_manage(request):
    """List all categories and allow creating a new one."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            if Category.objects.filter(name__iexact=name).exists():
                messages.error(request, f'Category "{name}" already exists.')
            else:
                Category.objects.create(name=name)
                messages.success(request, f'Category "{name}" created successfully! ✅')
        else:
            messages.error(request, 'Category name cannot be empty.')
        return redirect('category_manage')

    categories = Category.objects.all().order_by('name')
    return render(request, 'blogs/category_manage.html', {'categories': categories})


@login_required
def category_delete(request, pk):
    """Delete a category (only if it has no posts, or force-delete)."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        post_count = category.posts.count()
        if post_count > 0:
            messages.error(
                request,
                f'Cannot delete "{category.name}" — it has {post_count} post(s) assigned to it.'
            )
        else:
            category.delete()
            messages.success(request, f'Category deleted successfully.')
    return redirect('category_manage')
