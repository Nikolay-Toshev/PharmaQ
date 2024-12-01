from django import template

register = template.Library()

@register.filter
def unread_messages(user):
    all_messages = user.received_messages.all()
    for message in all_messages:
        if not message.is_read:
            return True