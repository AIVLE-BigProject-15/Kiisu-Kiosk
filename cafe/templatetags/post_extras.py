import os
from django import template
from django.conf import settings

register = template.Library()

@register.filter
def fix_route(value):
    return "/media" + os.sep + f"{os.sep}".join(value.path.split(os.sep)[-3:])


@register.filter
def fix_title(title):
    title = title.strip()
    if len(title) <= 7: return title
    print('\n'.join(title.split()))
    return '\n'.join(title.split())