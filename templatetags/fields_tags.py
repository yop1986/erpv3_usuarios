from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from datetime import date, datetime

from usuarios.personal_views import Configuracion

conf = Configuracion()
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


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    '''
    Returns verbose_name for a field.
    '''
    return instance._meta.get_field(field_name).verbose_name.title()

@register.simple_tag
def get_object_value(pObject, pField, pFormat=None):
    '''
    Se utiliza para obtener los valores de un objeto de forma dinámica
    '''
    value = getattr(pObject, pField)
    if isinstance(value, datetime):
        formato = conf.get_value('sitio', 'formato_fechahora')
        formato = pFormat if pFormat else formato
        return value.strftime(f'{formato}')
    elif isinstance(value, date):
        formato = conf.get_value('sitio', 'formato_fecha')
        formato = pFormat if pFormat else formato
        return value.strftime(formato)
    return mark_safe(value) if value else '-'

@register.simple_tag
def get_object_funcvalue(pObject, pField):
    '''
    Se utiliza para obtener los valores de un objeto de forma dinámica
    '''
    value = getattr(pObject, pField)()
    return mark_safe(value) if value else '-'