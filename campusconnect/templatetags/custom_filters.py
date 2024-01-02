# social_network/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def should_display_post(post, user):
    return not (post.shared_from and post.shared_from == user)
