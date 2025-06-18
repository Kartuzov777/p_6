from django.urls import path
from .views import PostList, PostDetail,PostSearch, NewsCreate, ArticleCreate, PostUpdate, PostDelete

urlpatterns = [
    path('news/', PostList.as_view(), name='post_list'),
    path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
# СОЗДАНИЕ
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),

# РЕДАКТИРОВАНИЕ
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='article_edit'),

# УДАЛЕНИЕ
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
]
