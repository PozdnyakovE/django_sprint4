from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post


class CustomUserCreationForm(UserCreationForm):
    """Форма для создания объекта пользователя."""

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name'
            ]


class UserUpdateForm(forms.ModelForm):
    """Форма для редактирования данных пользователя."""

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name'
            ]


class CommentForm(forms.ModelForm):
    """Форма для комментариев."""

    class Meta:
        model = Comment
        fields = ('text',) 


class PostForm(forms.ModelForm):
    """Форма для отображения объекта публикации."""

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
