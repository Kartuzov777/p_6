from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.core.mail import send_mail
from news.models import Post
from .models import Post
from .tasks import send_post_notification

@receiver(post_save, sender=User)
def add_user_to_common(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='common')
        instance.groups.add(group)

@receiver(user_signed_up)
def welcome_email(sender, request, user, **kwargs):
    send_mail(
        subject='Добро пожаловать в News Portal!',
        message='Спасибо за регистрацию на нашем портале новостей.',
        from_email='noreply@newsportal.com',
        recipient_list=[user.email],
        fail_silently=True,
    )

@receiver(post_save, sender=Post)
def notify_on_new_article(sender, instance, created, **kwargs):
    if created and instance.post_type == 'AR':  # только статьи, не новости
        categories = instance.categories.all()
        subscribers = set()

        for category in categories:
            for user in category.subscribers.all():
                subscribers.add(user.email)

        if subscribers:
            send_mail(
                subject=f"Новая статья: {instance.title}",
                message=f"{instance.preview()}\n\nЧитать: http://127.0.0.1:8000/news/{instance.id}/",
                from_email='noreply@newsportal.com',
                recipient_list=list(subscribers),
                fail_silently=True
            )

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created and instance.post_type == 'AR':  # Только статьи
        categories = instance.categories.all()
        emails = set()
        for cat in categories:
            for user in cat.subscribers.all():
                if user.email:
                    emails.add(user.email)
        if emails:
            send_post_notification.delay(
                list(emails),
                instance.title,
                instance.preview(),
                instance.id
            )


