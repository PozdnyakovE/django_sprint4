from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostsListView.as_view(), name='index'),
    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<post_id>/comment/',
         views.CommentCreateView.as_view(), name='add_comment'),
    path('posts/<post_id>/edit_comment/<comment_id>/',
         views.CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<post_id>/delete_comment/<comment_id>/',
         views.CommentDeleteView.as_view(), name='delete_comment'),
    path('category/<slug:category_slug>/',
         views.CategoryDetailView.as_view(), name='category_posts'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('profile/<username>/',
         views.UserDetailView.as_view(), name='profile'),
    path('edit_profile/',
         views.UserUpdateView.as_view(), name='edit_profile'),

]
