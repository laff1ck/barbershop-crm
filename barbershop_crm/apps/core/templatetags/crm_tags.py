from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def currency(value):
    try:
        val = float(value)
        return f"{val:,.0f} ₽".replace(',', ' ')
    except (TypeError, ValueError):
        return value


@register.filter
def stars(rating):
    """Render 5 star icons based on rating value."""
    try:
        filled = round(float(rating))
    except (TypeError, ValueError):
        filled = 0
    filled = max(0, min(5, filled))
    empty = 5 - filled
    html = (
        '<span class="text-warning">' + '<i class="bi bi-star-fill"></i>' * filled + '</span>'
        + '<span class="text-muted">' + '<i class="bi bi-star"></i>' * empty + '</span>'
    )
    return mark_safe(html)


@register.simple_tag
def status_badge(status, label):
    colors = {
        'pending':     'secondary',
        'confirmed':   'warning',
        'in_progress': 'info',
        'done':        'success',
        'cancelled':   'danger',
        'no_show':     'purple',
    }
    color = colors.get(status, 'secondary')
    return mark_safe(
        f'<span class="badge badge-status bg-{color} text-dark">{label}</span>'
    )
