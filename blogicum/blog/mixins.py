from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from .forms import CommentForm
from .models import Comment, Post


class ProfileUrlByUsername:
    """Возвращает URL профиля по указанному username."""

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username})


class UnauthorizedUsers(UserPassesTestMixin):
    """Проверка, является ли авторизованный пользователь автором."""

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect(reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.get_object().pk}))


class PostDeleteUpdateMixin:
    """Вспомогательный миксин для классов удаления, обновления поста."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentMixin:
    """Вспомогательный миксин для классов комментариев."""

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
