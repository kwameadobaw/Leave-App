from django import template
import re

register = template.Library()

@register.filter
def truncate_chars(value, max_length):
    """Truncate a string after a certain number of characters"""
    if not value:
        return ''
    
    max_length = int(max_length)
    if len(value) <= max_length:
        return value
    
    return value[:max_length].rsplit(' ', 1)[0] + '...'

@register.filter
def strip_tags(value):
    """Remove HTML tags from a string"""
    if not value:
        return ''
    
    return re.sub(r'<[^>]*>', '', value)

@register.filter
def capitalize_first(value):
    """Capitalize only the first letter of a string"""
    if not value:
        return ''
    
    return value[0].upper() + value[1:]