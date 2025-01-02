import re
from django import template

register = template.Library()

@register.filter
def clean_duration(iso_duration):
    match = re.match(r"PT(\d+)M([\d.]+)S", iso_duration)
    if match:
        minutes = int(match.group(1))
        seconds = round(float(match.group(2)))
        return f"{minutes}:{seconds:02d}"  # Formato "MM:SS"
    return "Formato inválido"
