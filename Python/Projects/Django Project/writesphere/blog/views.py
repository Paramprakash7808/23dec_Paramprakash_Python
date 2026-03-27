from django.shortcuts import render,redirect,get_object_or_404
from .models import Post
from .forms import PostForm,CommentForm

def post_list(request):

    posts = Post.objects.all().order_by('-created_at')

    return render(request,"blog/post_list.html",{'posts':posts})


def post_detail(request,id):

    post = get_object_or_404(Post,id=id)

    comments = post.comment_set.all()

    form = CommentForm()

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.user = request.user

            comment.post = post

            comment.save()

            return redirect('post_detail',id=id)

    return render(request,"blog/post_detail.html",
        {'post':post,'comments':comments,'form':form})


def create_post(request):

    if request.method == "POST":

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():

            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('/')

    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})