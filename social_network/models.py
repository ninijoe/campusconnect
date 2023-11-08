from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
import datetime
from django.utils import timezone
from django.dispatch import receiver





class User(AbstractUser):
    # Other fields and methods here

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_specific_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    department = models.CharField(max_length=50, blank=True)
    year_of_study = models.CharField(max_length=10, null=True, blank=True)
    bio = models.TextField(blank=True)
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')

    

    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def get_gender(self):
        return self.gender
    
    def get_department(self):
        return self.department
    
    def get_year_of_study(self):
        return self.year
    
    def get_bio(self):
        return self.bio
    

    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Format the 'created' timestamp to a user-friendly string
        formatted_time = self.created.strftime("%b %d, %Y %I:%M %p")
        return f"@{self.author}'s post- (' {self.content[:20]}..' ) {formatted_time}"
    



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Format the 'created' timestamp to a user-friendly string
        formatted_time = self.created.strftime("%b %d, %Y %I:%M %p")
        return f"@{self.user} commented on {self.post}, on {formatted_time}"
    



class Mention(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='mentions', null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='mentions', null=True)
    created = models.DateTimeField(auto_now_add=True)
