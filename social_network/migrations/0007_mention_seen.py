# Generated by Django 4.1.2 on 2023-12-28 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0006_post_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='mention',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
