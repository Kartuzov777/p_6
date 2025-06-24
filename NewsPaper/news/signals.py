from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.core.mail import send_mail

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