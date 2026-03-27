"""
Doctor Finder - Custom Template Tags
Practical 7: MVT pattern - custom template tags used in templates.
"""

from django import template

register = template.Library()


@register.filter
def currency_inr(value):
    """Display value as Indian Rupees."""
    try:
        return f"₹{float(value):,.2f}"
    except (TypeError, ValueError):
        return value


@register.filter
def availability_badge(availability):
    """Return Bootstrap badge class for availability status."""
    badges = {
        'available': 'bg-success',
        'busy': 'bg-warning text-dark',
        'on_leave': 'bg-danger',
    }
    return badges.get(availability, 'bg-secondary')


@register.simple_tag
def doctor_count():
    """Return total number of doctors."""
    from doctor.models import Doctor
    return Doctor.objects.count()
