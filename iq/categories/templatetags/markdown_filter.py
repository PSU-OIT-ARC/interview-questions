import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def frommarkdown(value):
    """
    Converts a string from Markdown to HTML
    """
    return mark_safe(markdown.markdown(value, safe_mode='replace'))
