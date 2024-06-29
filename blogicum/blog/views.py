from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.list import MultipleObjectMixin

from .forms import UserUpdateForm
from .models import Category, Post
from .utils import get_post_list


MAX_POSTS_ON_MAIN = 5


UserModel = get_user_model()


# def index(request):
#     post_list = get_post_list().filter(
#         category__is_published=True
#     )[:MAX_POSTS_ON_MAIN]
#     context = {'post_list': post_list}
#     return render(request, 'blog/index.html', context)


class PostsListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            category__is_published=True)


def post_detail(request, post_id):
    post = get_object_or_404(
        get_post_list().filter(
            category__is_published=True
        ).select_related('location', 'author'), pk=post_id
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_post(request, category_slug):
    category = get_object_or_404(
        Category.objects.values(
            'title', 'description'
        ).filter(is_published=True),
        slug=category_slug
    )
    post_list = get_post_list().filter(
        category__slug=category_slug
    )
    context = {'category': category,
               'post_list': post_list}
    return render(request, 'blog/category.html', context)


class PostCreateView(CreateView):
    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class UserDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = UserModel
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_object(self):
        # return UserModel.objects.get(username=self.kwargs.get("username"))
        return get_object_or_404(UserModel, username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):
        object_list = self.object.posts.select_related('author')
        context = super(UserDetailView, self).get_context_data(
            object_list=object_list, **kwargs)
        context['profile'] = self.object
        return context
    # success_url = reverse_lazy('blog:index')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModel
    template_name = 'blog/user.html'
    form_class = UserUpdateForm
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.object.user)
        return context