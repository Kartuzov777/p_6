from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment

user1 = User.objects.create_user(username='user1')
user2 = User.objects.create_user(username='user2')

author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

cat1 = Category.objects.create(name='Политика')
cat2 = Category.objects.create(name='Образование')
cat3 = Category.objects.create(name='Спорт')
cat4 = Category.objects.create(name='Наука')

post1 = Post.objects.create(author=author1, post_type='AR', title='Статья 1', content='Содержание статьи 1')
post2 = Post.objects.create(author=author2, post_type='AR', title='Статья 2', content='Содержание статьи 2')
post3 = Post.objects.create(author=author1, post_type='NW', title='Новость 1', content='Содержание новости 1')

post1.categories.add(cat1, cat2)
post2.categories.add(cat3)
post3.categories.add(cat4)

comment1 = Comment.objects.create(post=post1, user=user2, content='Комментарий к статье 1 от user2')
comment2 = Comment.objects.create(post=post2, user=user1, content='Комментарий к статье 2 от user1')
comment3 = Comment.objects.create(post=post3, user=user2, content='Комментарий к новости от user2')
comment4 = Comment.objects.create(post=post1, user=user1, content='Комментарий к статье 1 от user1')

post1.like()
post1.like()
post2.dislike()
post3.like()

comment1.like()
comment2.dislike()
comment3.like()
comment4.like()

author1.update_rating()
author2.update_rating()

best_author = Author.objects.order_by('-rating').first()
print(f"Лучший пользователь: {best_author.user.username}, рейтинг: {best_author.rating}")

best_post = Post.objects.order_by('-rating').first()
print(f"Дата: {best_post.created_at}")
print(f"Автор: {best_post.author.user.username}")
print(f"Рейтинг: {best_post.rating}")
print(f"Заголовок: {best_post.title}")
print(f"Превью: {best_post.preview()}")

comments = Comment.objects.filter(post=best_post)
for c in comments:
    print(f"\nДата: {c.created_at}")
    print(f"Пользователь: {c.user.username}")
    print(f"Рейтинг: {c.rating}")
    print(f"Текст: {c.content}")