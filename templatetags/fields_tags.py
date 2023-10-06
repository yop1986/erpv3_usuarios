from django.utils.translation import gettext as _

from django import template
register = template.Library()

@register.filter
def verbose_name(value):
    return value._meta.verbose_name

@register.filter
def verbose_name_plural(value):
    return value._meta.verbose_name_plural

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()

@register.simple_tag
def get_descripcion_estados(value, tipo=1):
    if tipo == 1:
        return _('Activo') if value else _('Inactivo')
    else:
        return _('Vigente') if value else _('No vigente')