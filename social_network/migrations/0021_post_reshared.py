# Generated by Django 4.1.2 on 2024-01-02 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0020_alter_resharedpost_original_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reshared',
            field=models.BooleanField(default=False),
        ),
    ]
