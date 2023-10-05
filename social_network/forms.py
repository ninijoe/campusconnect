from django import forms
from .models import User
from .models import Post
from .models import Comment

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Write your post here...' , 'style': 'width: 67%;'}),
        label='',
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Comment',
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

   

class FollowForm(forms.Form):
    user_to_follow = forms.IntegerField(widget=forms.HiddenInput)


class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_photo']
