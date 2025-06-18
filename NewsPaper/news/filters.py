import django_filters
from django.forms import DateInput
from .models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Заголовок')
    author__user__username = django_filters.CharFilter(label='Автор')
    created_at = django_filters.DateFilter(
        lookup_expr='gte',
        label='Позже даты',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'created_at']