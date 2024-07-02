from datetime import date
from itertools import count
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.list import MultipleObjectMixin

from .forms import CommentForm, PostForm, UserUpdateForm
from .models import Category, Comment, Post
from .utils import get_post_list


MAX_POSTS_ON_MAIN = 10


UserModel = get_user_model()


# def index(request):
#     post_list = get_post_list().filter(
#         category__is_published=True
#     )[:MAX_POSTS_ON_MAIN]
#     context = {'post_list': post_list}
#     return render(request, 'blog/index.html', context)


class PostsListView(ListView):
    # model = Post
    template_name = 'blog/index.html'
    paginate_by = MAX_POSTS_ON_MAIN

    def get_queryset(self):
        return get_post_list().filter(
            category__is_published=True)


# def post_detail(request, post_id):
#     post = get_object_or_404(
#         get_post_list().filter(
#             category__is_published=True
#         ).select_related('location', 'author'), pk=post_id
#     )
#     context = {'post': post}
#     return render(request, 'blog/detail.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(
            Post, pk=self.kwargs['post_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context 

    # def get_object(self):
    #     return get_object_or_404(
    #         get_post_list().filter(
    #             category__is_published=True
    #             ).select_related('location', 'author'),
    #         pk=self.kwargs['post_id'])
    
    # def get_context_data(self, **kwargs):
    #     context = super(PostDetailView, self).get_context_data()
    #     post = get_object_or_404(
    #         get_post_list().filter(
    #             category__is_published=True
    #             ).select_related('location', 'author'),
    #         pk=self.kwargs['post_id'])
    #     context = {'post': post}
    #     return context
        

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
    
# def category_post(request, category_slug):
#     category = get_object_or_404(
#         Category.objects.values(
#             'title', 'description'
#         ).filter(is_published=True),
#         slug=category_slug
#     )
#     # post_list = get_post_list().filter(
#     #     category__slug=category_slug
#     # )
#     # context = {'category': category,
#     #            'post_list': post_list}
#     context = {'category': category}
#     return render(request, 'blog/category.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_published = True
        # form.instance.pub_date = date.today()
        return super().form_valid(form) 

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username})
    

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    # form_class = PostForm
    fields = ('title', 'text', 'location', 'category', 'image', )
    template_name = 'blog/create.html'

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 
    
    # def get_success_url(self):
    #     return reverse_lazy(
    #         'blog:profile',
    #         kwargs={'username': self.request.user.username})
    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.object.pk})
    

class PostDeleteView(LoginRequiredMixin, DeleteView):

    model = Post
    # form_class = PostForm
    template_name = 'blog/create.html'

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context
    
    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username})



class UserDetailView(DetailView, MultipleObjectMixin):
    model = UserModel
    template_name = 'blog/profile.html'
    paginate_by = MAX_POSTS_ON_MAIN
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(UserModel, username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):
        object_list = self.object.posts.annotate(comment_count=Count('comments')).select_related('author').order_by('-pub_date')
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
    
    

class CommentCreateView(LoginRequiredMixin, CreateView):
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
    

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    related_post = None
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.related_post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(
            Comment,
            pk=self.kwargs['comment_id'],
            )
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.related_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.related_post.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    related_post = None
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.related_post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(
            Comment,
            pk=self.kwargs['comment_id'],
            )
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.related_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.related_post.pk})