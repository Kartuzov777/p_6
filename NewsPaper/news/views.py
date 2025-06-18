from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django_filters.views import FilterView
from .filters import PostFilter
from django.urls import reverse_lazy
from .forms import PostForm

class PostList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetail(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'

class PostSearch(FilterView):
    model = Post
    template_name = 'news/post_search.html'
    context_object_name = 'posts'
    filterset_class = PostFilter
    paginate_by = 10

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        post.author = self.request.user.author
        return super().form_valid(form)

class ArticleCreate(NewsCreate):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        post.author = self.request.user.author
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')

