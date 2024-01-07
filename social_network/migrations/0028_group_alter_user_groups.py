# Generated by Django 4.1.2 on 2024-01-06 04:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0027_user_student_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('members', models.ManyToManyField(blank=True, help_text='Members of this group.', related_name='group_members', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_accept_join_group_requests', 'Can accept join group requests'), ('can_make_member_moderator', 'Can make a member a moderator'), ('can_delete_group_post', 'Can delete group post'), ('can_ban_group_user', 'Can ban a user from the group')],
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_groups', to='social_network.group'),
        ),
    ]