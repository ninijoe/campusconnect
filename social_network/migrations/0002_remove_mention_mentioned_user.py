# Generated by Django 4.1.2 on 2023-10-08 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mention',
            name='mentioned_user',
        ),
    ]