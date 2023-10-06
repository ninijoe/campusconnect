from django import template

register = template.Library()

@register.filter
def startswith_user_profile(view_name):
    return view_name.startswith('user_profile')
