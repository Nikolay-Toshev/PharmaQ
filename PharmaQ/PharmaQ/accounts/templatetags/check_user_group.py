from django import template

register = template.Library()

@register.filter()
def check_user_group(user, group):
    return user.groups.filter(name=group).exists()
