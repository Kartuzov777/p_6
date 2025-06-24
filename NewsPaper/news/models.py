from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Суммарный рейтинг всех постов автора * 3
        post_rating = sum(post.rating for post in self.post_set.all()) * 3
        # Суммарный рейтинг всех комментариев автора
        comment_rating = sum(comment.rating for comment in self.user.comment_set.all())
        # Суммарный рейтинг всех комментариев под постами автора
        comments_on_posts_rating = sum(
            comment.rating for post in self.post_set.all() for comment in post.comment_set.all()
        )
        self.rating = post_rating + comment_rating + comments_on_posts_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(
        to='auth.User',
        related_name='subscribed_categories',
        blank=True
    )
    def __str__(self):
        return self.name


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=NEWS)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, through='PostCategory')

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created and instance.post_type == 'AR':  # только статьи
        categories = instance.category.all()
        for category in categories:
            for user in category.subscribers.all():
                send_mail(
                    subject=f"Новая статья в категории {category.name}",
                    message=f"{instance.title}\n{instance.preview()}\nСсылка: http://127.0.0.1:8000/news/{instance.id}/",
                    from_email='noreply@newssite.com',
                    recipient_list=[user.email],
                )