from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_all_answers(context):
    pharmacist = context['pharmacist']
    number_of_answers = pharmacist.answers.count()
    return number_of_answers