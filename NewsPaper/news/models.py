from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    def update_rating(self):
        post_rating = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] * 3
        comment_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        comments_under_post_rating = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']

        self.rating = post_rating + comment_rating + comments_under_post_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(max_length=64, default='All', unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.category_name


class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('article', 'статья'),
        ('news', 'новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=15, choices=POST_TYPE_CHOICES)
    date_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.FloatField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    @property
    def preview(self):
        if len(self.content) > 124:
            return self.content[:124] + '...'
        else:
            return self.content

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Piece_Of_News_Detail', args=[str(self.id)])


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        if len(self.text) < 100:
            return self.text
        return self.text[:100] + '...'

