# Generated by Django 4.1.2 on 2024-01-09 04:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0043_remove_grouppost_image_grouppost_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grouppost',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.AddField(
            model_name='grouppost',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='group_tagged_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tagged_users', to=settings.AUTH_USER_MODEL),
        ),
    ]