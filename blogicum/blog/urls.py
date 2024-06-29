from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostsListView.as_view(), name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_post, name='category_posts'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('profile/<slug:username>/',
         views.UserDetailView.as_view(), name='profile'),
    path('profile/edit/',
         views.UserUpdateView.as_view(), name='edit_profile'),

]
