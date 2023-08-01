from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment
from django.db import models

def like_post(modeladmin, request, queryset):
    queryset.update(rating=models.F('rating') + 1)

like_post.short_description = "Лайк"
# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'content', 'author', 'post_type', 'rating', 'date_time')
    list_filter = ('date_time',)
    search_fields = ('title', 'author__user__username', 'rating')
    actions = [like_post]


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
