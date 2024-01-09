from django import forms
from .models import User
from .models import Post
from .models import Comment
from django.contrib.auth.forms import UserChangeForm , PasswordChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.utils.safestring import mark_safe
from .models import Group
import bleach

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'bio', 'group_photo']
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 30, 'rows': 5}),  # Adjust the 'cols' value as needed
        }


class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'bio', 'group_photo']


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

class CustomPasswordResetForm(PasswordResetForm):
    # Add any customizations if needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form fields if necessary

class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(label='New Email', max_length=254)

class ChangeUsernameForm(UserChangeForm):
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ['username']
        

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Validate the password
        user = authenticate(username=self.instance.username, password=password)
        if not user or not user.check_password(password):
            raise forms.ValidationError("Invalid password. Please enter the correct password.")

        return cleaned_data


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User


class DepartmentForm(forms.Form):
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))




    




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'photo', 'video', 'tags', 'location']

    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Write your post here...'}),
        label='',
    )

    
    def as_p_with_icon(self):
        return mark_safe(''.join([
            '<div class="form-group">',
            str(self['content']),  # Render the content field
            '</div>',
            '<div class="form-group">',
            '<label for="id_photo">Photo: </label>',
            str(self['photo']),  # Render photo field in its own row
            '</div>',
            '<div class="form-group">',
            '<label for="id_video">Video: </label>',
            str(self['video']),  # Render video field in its own row
            '</div>',
            '<div class="form-group">',
            '<label for="id_tags">Tags: </label>',
            str(self['tags']),  # Render tags field in its own row
            '</div>',
            '<div class="form-group">',
            '<label for="id_location">Location: </label>',
            str(self['location']),  # Render location field in its own row
            '</div>',
        ]))
    
    









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



