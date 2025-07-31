from django.contrib import admin
from blog.models import Post, Tag, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ["post", "author"]
    list_display = ["author"]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ["tags", "author", "likes"]
    list_display = ["comments"]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

