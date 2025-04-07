from django import template

register = template.Library()


@register.filter
def format_time(value):
    try:
        total_seconds = int(value.total_seconds())
        dias = total_seconds // 86400  # 86400 segundos en un día
        horas = (total_seconds % 86400) // 3600
        minutos = (total_seconds % 3600) // 60

        partes = []
        if dias > 0:
            partes.append(f"{dias}d")
        if horas > 0 or dias > 0:
            partes.append(f"{horas}h")
        partes.append(f"{minutos}m")

        return " ".join(partes)
    except Exception:
        return ""
