from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from datetime import date

register = template.Library()

@register.filter
def verbose_name(value):
    return value._meta.verbose_name

@register.filter
def verbose_name_plural(value):
    return value._meta.verbose_name_plural

@register.simple_tag
def get_descripcion_estados(value, tipo=1):
    if tipo == 1:
        return _('Activo') if value else _('Inactivo')
    else:
        return _('Vigente') if value else _('No vigente')


# Utilizado en:
#   - QlikSense
@register.simple_tag
def get_verbose_field_name(instance, field_name):
    '''
    Returns verbose_name for a field.
    '''
    return instance._meta.get_field(field_name).verbose_name.title()

# Utilizado en:
#   - QlikSense
@register.simple_tag
def get_object_value(pObject, pField, pFormat=None):
    '''
    Se utiliza para obtener los valores de un objeto de forma dinámica
    '''
    value = getattr(pObject, pField)
    if isinstance(value, date):
        formato = pFormat if pFormat else "%d/%m/%Y"
        return value.strftime(formato)
    return mark_safe(value) if value else '-'

# Utilizado en:
#   - QlikSense
@register.simple_tag
def get_object_funcvalue(pObject, pField):
    '''
    Se utiliza para obtener los valores de un objeto de forma dinámica
    '''
    value = getattr(pObject, pField)()
    return mark_safe(value) if value else '-'