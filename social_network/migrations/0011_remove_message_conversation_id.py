# Generated by Django 4.1.2 on 2023-12-30 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0010_user_public_key_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='conversation_id',
        ),
    ]
