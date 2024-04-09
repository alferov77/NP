from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Subscriber, Post
from django.conf import settings


@shared_task
def send_new_post_notification(post_id):
    post = Post.objects.get(id=post_id)
    subscribers = Subscriber.objects.filter(category__in=post.categories.all())

    subject = f'New post: {post.title}'
    context = {
        'post': post,
    }
    html_content = render_to_string('news/email_new_post.html', context)
    text_content = strip_tags(html_content)

    for subscriber in subscribers:
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [subscriber.user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()


@shared_task
def send_weekly_newsletter():
    one_week_ago = timezone.now() - timezone.timedelta(weeks=1)
    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        posts = Post.objects.filter(
            categories__in=subscriber.category.all(),
            creation_date__gte=one_week_ago
        ).distinct()

        if posts.exists():
            subject = 'Еженедельная рассылка!'
            context = {'posts': posts}
            html_content = render_to_string('news/weekly_newsletter.html', context)
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.user.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
