# social_network/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def should_display_post(post, user):
    return not (post.shared_from and post.shared_from == user)

@register.filter(name='is_reshared_by_user')
def is_reshared_by_user(post, user):
    return post.is_reshared_by_user(user)

@register.filter
def user_has_liked(comment, user):
    return comment.likes.filter(id=user.id).exists()
