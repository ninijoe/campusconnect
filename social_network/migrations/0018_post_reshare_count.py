# Generated by Django 4.1.2 on 2024-01-01 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0017_resharedpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reshare_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
