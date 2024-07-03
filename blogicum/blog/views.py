from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import MultipleObjectMixin

from .forms import CommentForm, PostForm, UserUpdateForm
from .models import Category, Comment, Post
from .utils import get_post_list


UserModel = get_user_model()
MAX_POSTS_ON_MAIN = 10


class PostsListView(ListView):
    template_name = 'blog/index.html'
    paginate_by = MAX_POSTS_ON_MAIN

    def get_queryset(self):
        return get_post_list().filter(
            category__is_published=True)


class PostObjectMixin:
    model = Post

    def get_object(self):
        return get_object_or_404(
            Post, pk=self.kwargs['post_id'])


class PostDetailView(PostObjectMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_published = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username})


class PostDeleteUpdateMixin(PostObjectMixin):
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PostDeleteUpdateMixin, LoginRequiredMixin, UpdateView):
    fields = ('title', 'text', 'location', 'category', 'image', )

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.object.pk})


class PostDeleteView(PostDeleteUpdateMixin,
                     LoginRequiredMixin, DeleteView, ModelFormMixin):
    form_class = PostForm

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username})


class CategoryDetailView(DetailView, MultipleObjectMixin):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = MAX_POSTS_ON_MAIN

    def get_object(self, *args, **kwargs):
        return get_object_or_404(
            Category, slug=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        object_list = get_post_list().filter(
            category__slug=self.kwargs['category_slug'])
        context = super(CategoryDetailView, self).get_context_data(
            object_list=object_list, **kwargs)
        return context


class UserDetailView(DetailView, MultipleObjectMixin):
    model = UserModel
    template_name = 'blog/profile.html'
    paginate_by = MAX_POSTS_ON_MAIN
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(UserModel, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        object_list = self.object.posts.annotate(
            comment_count=Count('comments')).select_related('author').order_by(
                '-pub_date')
        if self.request.user != self.object:
            object_list = object_list.filter(
                is_published=True, pub_date__lte=date.today())
        context = super(UserDetailView, self).get_context_data(
            object_list=object_list, **kwargs)
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModel
    template_name = 'blog/user.html'
    form_class = UserUpdateForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username})


class CommentMixin:
    related_post = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.related_post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.related_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.related_post.pk})


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    pass


class CommentUpdateDeleteMixin:
    template_name = 'blog/comment.html'

    def get_object(self):
        return get_object_or_404(
            Comment,
            pk=self.kwargs['comment_id'],
            )
    

class CommentUpdateView(CommentMixin, CommentUpdateDeleteMixin,
                        LoginRequiredMixin, UpdateView):
    pass


class CommentDeleteView(CommentMixin, CommentUpdateDeleteMixin,
                        LoginRequiredMixin, DeleteView):
    pass
