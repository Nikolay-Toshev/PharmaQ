from django import template

from PharmaQ.accounts.utils import get_pharmacist_rating

register = template.Library()

@register.simple_tag(takes_context=True)
def calculate_rating(context):
    pharmacist = context['pharmacist']
    rating = get_pharmacist_rating(pharmacist)
    return rating