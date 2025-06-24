from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from news.models import Post, Category

class Command(BaseCommand):
    help = 'Send weekly digest to subscribers'

    def handle(self, *args, **kwargs):
        one_week_ago = now() - timedelta(days=7)
        posts = Post.objects.filter(created_at__gte=one_week_ago, post_type='AR')  # только статьи

        categories = Category.objects.all()
        for category in categories:
            category_posts = posts.filter(categories=category)
            if category_posts.exists():
                subscriber_emails = [user.email for user in category.subscribers.all()]
                if subscriber_emails:
                    post_list = "\n".join([
                        f"{post.title}: http://127.0.0.1:8000/news/{post.id}/"
                        for post in category_posts
                    ])
                    send_mail(
                        subject=f"Статьи за неделю в категории: {category.name}",
                        message=post_list,
                        from_email='noreply@newsportal.com',
                        recipient_list=subscriber_emails,
                    )