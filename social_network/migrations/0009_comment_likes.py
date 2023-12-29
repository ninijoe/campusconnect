# Generated by Django 4.1.2 on 2023-12-29 11:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0008_user_blocked_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
