import os
from django import template
from django.conf import settings

register = template.Library()

@register.filter
def fix_route(value):
    return "/media" + os.sep + f"{os.sep}".join(value.path.split(os.sep)[-3:])