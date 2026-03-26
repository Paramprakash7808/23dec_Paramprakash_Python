from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('author', 'Author'),
        ('reader', 'Reader'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='reader')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_admin_user(self):
        return self.role == 'admin' or self.is_staff or self.is_superuser

    def is_author(self):
        return self.role == 'author'

    def is_reader(self):
        return self.role == 'reader'

    def get_follower_count(self):
        return self.followers.count()

    def get_following_count(self):
        return self.following.count()

    def get_post_count(self):
        return self.blog_posts.filter(status='published').count()


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, related_name='following', on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        CustomUser, related_name='followers', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
