from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def rfc3339(value):
    date_str = value.isoformat() if value else ""
    return mark_safe(f'<span class="isodate">{date_str}</span>')
