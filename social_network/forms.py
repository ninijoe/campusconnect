from django import forms
from .models import User
from .models import Post
from .models import Comment

from django import forms
from .models import Post

DEPARTMENT_CHOICES = [
    ('ABE', 'ABE (Adult Basic Education)'),
    ('Design', 'Design and Performing Arts'),
    ('Arts', 'Arts and Social Sciences'),
    ('Business', 'Business and Management'),
    ('Education', 'Education'),
    ('ESL', 'ESL (English as a Second Language)'),
    ('EXPO', 'EXPO (Exploratory Studies)'),
    ('Health', 'Health Sciences'),
    ('HighSchool', 'High School @ VIU'),
    ('HumanServices', 'Human Services'),
    ('Indigenous', 'Indigenous Studies'),
    ('Science', 'Science, Engineering and Technology'),
    ('Trades', 'Trades and Applied Technology'),
    ('Tourism', 'Tourism, Recreation and Hospitality'),
]


class DepartmentForm(forms.Form):
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Write your post here...' , 'style': 'width: 85%;'}),
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
