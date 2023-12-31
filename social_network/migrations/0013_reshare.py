# Generated by Django 4.1.2 on 2024-01-01 02:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0012_post_shared_from'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reshare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('original_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reshares', to='social_network.post')),
                ('reshared_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reshared_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
