from django import forms
from  django.contrib.auth import get_user_model

from .models import Comment


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
