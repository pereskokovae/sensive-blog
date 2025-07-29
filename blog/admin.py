from django.contrib import admin
from blog.models import Post, Tag, Comment


class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ["post", "author"]


class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ["tags", "author", "likes"]
    list_display = ["comments"]


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
