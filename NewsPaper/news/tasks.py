from celery import shared_task
from django.core.mail import send_mail
from datetime import timedelta, datetime
from django.utils import timezone
from .models import Post, Category
from django.contrib.auth.models import User

@shared_task
def send_post_notification(emails, title, preview, post_id):
    send_mail(
        subject=f"Новая статья: {title}",
        message=f"{preview}\n\nЧитать: http://127.0.0.1:8000/news/{post_id}/",
        from_email='noreply@newsportal.com',
        recipient_list=emails,
    )


@shared_task
def send_post_notification(emails, title, preview, post_id):
    send_mail(
        subject=f'Новая статья: {title}',
        message=f'{preview}\n\nЧитать статью: http://127.0.0.1:8000/news/{post_id}/',
        from_email='noreply@newsportal.com',
        recipient_list=emails,
    )

@shared_task
def weekly_digest():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week, post_type='AR')

    categories = Category.objects.all()
    for category in categories:
        category_posts = posts.filter(categories=category)
        if not category_posts.exists():
            continue

        emails = category.subscribers.values_list('email', flat=True)

        post_list = '\n'.join([
            f"- {p.title}: http://127.0.0.1:8000/news/{p.id}/"
            for p in category_posts
        ])

        send_mail(
            subject=f"Еженедельная рассылка по категории '{category.name}'",
            message=f"Статьи за неделю:\n\n{post_list}",
            from_email='noreply@newsportal.com',
            recipient_list=emails,
        )