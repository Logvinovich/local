from django.contrib import admin
from .models import Post, Comment, Category, DisposableCode, PostCategory


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(DisposableCode)
admin.site.register(PostCategory)