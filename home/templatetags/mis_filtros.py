from django import template

register = template.Library()


@register.filter
def format_time(value):
    try:
        total_seconds = int(value.total_seconds())
        horas = total_seconds // 3600
        minutos = (total_seconds % 3600) // 60
        return f"{horas}h {minutos}m"
    except Exception:
        return ""
