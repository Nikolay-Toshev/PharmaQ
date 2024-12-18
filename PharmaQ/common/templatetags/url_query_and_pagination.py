from django import template

register = template.Library()

@register.simple_tag
def url_query_and_pagination(request, key, value):
    query_string = request.GET.copy()
    query_string[key] = value
    return query_string.urlencode()