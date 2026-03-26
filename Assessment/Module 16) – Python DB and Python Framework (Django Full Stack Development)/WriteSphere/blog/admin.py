from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Category, Comment, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        return obj.get_post_count()
    post_count.short_description = "Published Posts"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'views', 'created_at', 'cover_preview')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    raw_id_fields = ('author',)
    list_editable = ('status',)
    actions = ['publish_posts', 'draft_posts']

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;" />', obj.cover_image.url)
        return "No Image"
    cover_preview.short_description = "Cover"

    def publish_posts(self, request, queryset):
        queryset.update(status='published')
        self.message_user(request, f"{queryset.count()} posts published.")
    publish_posts.short_description = "Publish selected posts"

    def draft_posts(self, request, queryset):
        queryset.update(status='draft')
        self.message_user(request, f"{queryset.count()} posts set to draft.")
    draft_posts.short_description = "Set selected posts to Draft"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'short_content', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('author__username', 'content', 'post__title')
    list_editable = ('is_approved',)
    actions = ['approve_comments', 'disapprove_comments']

    def short_content(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    short_content.short_description = "Content"

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected comments approved.")
    approve_comments.short_description = "Approve selected comments"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Selected comments disapproved.")
    disapprove_comments.short_description = "Disapprove selected comments"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')


# Customize admin site header
admin.site.site_header = "WriteSphere Admin"
admin.site.site_title = "WriteSphere Admin Portal"
admin.site.index_title = "Welcome to WriteSphere Administration"
