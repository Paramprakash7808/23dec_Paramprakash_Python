from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(max_length=200)

    content = models.TextField()

    image = models.ImageField(upload_to='posts', blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):

    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):

    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    user = models.ForeignKey(User,on_delete=models.CASCADE)


class Follow(models.Model):

    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")

    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")