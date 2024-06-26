from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .tasks import send_new_post_notification

from django.core.cache import cache



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.post_set.aggregate(models.Sum('rating'))['rating__sum'] * 3
        comments_rating = self.user.comment_set.aggregate(models.Sum('rating'))['rating__sum']
        posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum']
        self.rating = posts_rating + (comments_rating or 0) + (posts_comments_rating or 0)
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    POST_TYPES = [
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    creation_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        formatted_date = self.creation_date.strftime('%Y-%m-%d %H:%M')
        return f'Author: {self.author.user.username}, Date: {formatted_date}, Title: {self.title}, Preview: {self.text[:124]}...'

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.pk})


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )



@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        from .tasks import send_new_post_notification
        send_new_post_notification.delay(instance.id)

@receiver(post_save, sender=Post)
def clear_cache(sender, instance, **kwargs):
    cache.delete(f'post_{instance.pk}')

@receiver(post_delete, sender=Post)
def clear_cache_delete(sender, instance, **kwargs):
    cache.delete(f'post_{instance.pk}')