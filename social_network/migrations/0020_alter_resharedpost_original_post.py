# Generated by Django 4.1.2 on 2024-01-01 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0019_alter_resharedpost_original_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resharedpost',
            name='original_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reshares', to='social_network.post'),
        ),
    ]
