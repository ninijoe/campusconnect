from django import template

register = template.Library()

@register.filter
def startswith_user_profile(view_name):
    return view_name.startswith('user_profile')



@register.filter
def should_display_post(post, user):
    return not (post.shared_from and post.shared_from == user)