from django import template
from datetime import datetime, date

register = template.Library()

@register.filter
def friendly_date(value):
    """Convert a date to a user-friendly format"""
    if not value:
        return ''
    
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            return value
    
    today = date.today()
    
    # If it's today
    if value == today:
        return 'Today'
    
    # If it's tomorrow
    if value == today.replace(day=today.day + 1):
        return 'Tomorrow'
    
    # If it's yesterday
    if value == today.replace(day=today.day - 1):
        return 'Yesterday'
    
    # Otherwise return formatted date
    return value.strftime('%d %b, %Y')

@register.filter
def date_range_days(start_date, end_date):
    """Calculate the number of days in a date range, inclusive"""
    if not start_date or not end_date:
        return 0
    
    if isinstance(start_date, str):
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            return 0
    
    if isinstance(end_date, str):
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return 0
    
    delta = end_date - start_date
    return delta.days + 1  # +1 to include both start and end dates

@register.filter
def status_badge_class(status):
    """Return the appropriate Bootstrap badge class based on status"""
    status_classes = {
        'pending': 'bg-warning',
        'approved': 'bg-success',
        'rejected': 'bg-danger'
    }
    return status_classes.get(status.lower(), 'bg-secondary')