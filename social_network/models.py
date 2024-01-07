from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
import datetime
from django.utils import timezone
from django.dispatch import receiver
import gnupg
from cryptography.fernet import Fernet





class User(AbstractUser):
    # Other fields and methods here

    groups = models.ManyToManyField(
        'social_network.Group',
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

    student_email = models.EmailField(blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    department = models.CharField(max_length=50, blank=True)
    year_of_study = models.CharField(max_length=10, null=True, blank=True)
    bio = models.TextField(blank=True)
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')
    blocked_users = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='blocked_by_users')
    public_key = models.TextField(blank=True, null=True)
    

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
    
    
    def generate_key_pair(self):
        # Generate GPG key pair for the user
        gpg = gnupg.GPG()
        key_data = gpg.gen_key_input(
            name_email=self.email,
            passphrase=self.password,  # Use a better way to handle passphrase
        )
        key = gpg.gen_key(key_data)
        self.public_key = str(key)
        self.save()

    def get_public_key(self):
        return self.public_key
    




class Group(models.Model):
    name = models.CharField(max_length=255, unique=True, default='')
    bio = models.TextField(blank=True)
    creator = models.ForeignKey(
        'social_network.User',
        on_delete=models.CASCADE,
        related_name='created_groups',
        null=True,
        blank=True,
        help_text='The user who created the group.'
    )
    members = models.ManyToManyField(
        'social_network.User',
        related_name='group_memberships',
        blank=True,
        help_text='Members of this group.'
    )
    moderators = models.ManyToManyField(
        'social_network.User',
        related_name='group_moderators',
        blank=True,
        help_text='Moderators of this group.'
    )
    group_photo = models.ImageField(upload_to='group_photos/', null=True, blank=True)
    created = models.DateTimeField(default=timezone.now, editable=False, help_text='The date and time the group was created.')

    




class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    encrypted_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def encrypt_content(self, content, key):
        # Encrypt message content using Fernet symmetric key encryption
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(content.encode())
        return encrypted_data.decode()

    def decrypt_content(self, key):
        # Decrypt message content using Fernet symmetric key encryption
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(self.encrypted_content.encode())
        return decrypted_data.decode()

    def save(self, *args, **kwargs):
        if not self.sender.public_key:
            self.sender.generate_key_pair()

        recipient_public_key = self.recipient.get_public_key()
        self.encrypted_content = self.encrypt_content(self.content, recipient_public_key)

        super().save(*args, **kwargs)

    def get_decrypted_content(self):
        if self.is_read:
            recipient_private_key = self.recipient.password  # Use a better way to handle private key
            return self.decrypt_content(recipient_private_key)
        return "This message has not been read yet."







class ResharedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reshared_posts')
    original_post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='reshares')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} reshared {self.original_post} on {self.created}"

    def is_reshared_by_user(self, user):
        return self.reshares.filter(user=user).exists()






class PostMedia(models.Model):
    photo = models.ImageField(upload_to='post_media/', null=True, blank=True)
    video = models.FileField(upload_to='post_media/', null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"PostMedia - ID: {self.id}"

    def delete(self, *args, **kwargs):
        # Delete associated media files from storage
        if self.photo:
            self.photo.delete(save=False)
        if self.video:
            self.video.delete(save=False)
        super().delete(*args, **kwargs)




    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    reshare_count = models.PositiveIntegerField(default=0)
    reshared = models.BooleanField(default=False)  # Add this field
    media = models.OneToOneField(PostMedia, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        formatted_time = self.created.strftime("%b %d, %Y %I:%M %p")
        return f"@{self.author}'s post- (' {self.content[:20]}..' ) {formatted_time}"

    def mark_as_reshared(self):
        self.reshared = True
        self.save()

    def increase_reshare_count(self):
        self.reshare_count += 1
        self.save()

    def delete(self, *args, **kwargs):
        # Delete associated media when post is deleted
        if self.media:
            self.media.delete()
        super().delete(*args, **kwargs)

    


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)


    def __str__(self):
        # Format the 'created' timestamp to a user-friendly string
        formatted_time = self.created.strftime("%b %d, %Y %I:%M %p")
        return f"@{self.user} commented on {self.post}, on {formatted_time}"
    



class Mention(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='mentions', null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='mentions', null=True)
    created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)  # Add this line to include the 'seen' field