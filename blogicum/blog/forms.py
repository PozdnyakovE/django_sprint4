from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name'
            ]
        

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name'
            ]
        

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('text',) 


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }