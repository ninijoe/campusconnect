# Generated by Django 4.1.2 on 2023-12-31 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0011_remove_message_conversation_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='shared_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shared_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
