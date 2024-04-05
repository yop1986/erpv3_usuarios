import uuid
import datetime
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from simple_history.models import HistoricalRecords


class Usuario(AbstractUser, PermissionsMixin):
    '''
        Información propia del usuario, asociada a la cuenta y accesos
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name_description = _('Nombre Completo')
    #is_active_description = _('Estado')

    class Meta:
        pass
        #permissions = [
        #    ('create_usuario', 'Permite la creación de usuarios'),
        #]
    def clean(self):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()

    def __str__(self):
        return f'{self.get_full_name()} ({self.username})'

    def get_grupos(self):
        return list(self.groups.all().order_by('name'))

    def get_estado(self):
        return 'Activo' if self.is_active else 'Inactivo'
    
class Perfil(models.Model):
    '''
        Información adicional del usuario
    '''
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telefono= models.CharField(_('Telefono'), max_length=12, blank=True)
    celular = models.CharField(_('Celular'), max_length=12, blank=True)
    dpi     = models.CharField(_('DPI'), max_length=13, blank=True)
    nit     = models.CharField(_('Nit'), max_length=10, blank=True)
    fecha_nacimiento = models.DateField(_('Fecha de nacimiento'), null=True, blank=True)
    
    usuario = models.OneToOneField(Usuario, verbose_name='Perfil', on_delete = models.CASCADE)

    edad_description = _('Edad')

    def __str__(self):
        return f'Perfil: {self.usuario.username}'

    def get_edad(self):
        return relativedelta(datetime.date.today(), self.fecha_nacimiento).years

@receiver(post_save, sender=Usuario)
def create_usuario_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=Usuario)
def save_usuario_perfil(sender, instance, **kwargs):
    instance.perfil.save()



class Puesto(models.Model):
    '''
        Estrcutura organizacional de la empresa
    '''
    ESTADOS = [
        ('V', 'Vigente'),
        ('B', 'Bloqueada'),
        ('E', 'Eliminada'),
    ]
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo  = models.CharField(_('Código'), max_length=12)
    nombre  = models.CharField(_('Nombre'), max_length=30)
    estado  = models.CharField(_('Estado'), choices=ESTADOS, max_length=1)
    # def_estado_display()
    actualizado = models.DateTimeField(_('Ult. Actualizacion'), auto_now=True)

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='perfil', on_delete=models.PROTECT, null=True, blank=True)
    padre   = models.ForeignKey('self', related_name='puesto_superior', on_delete=models.RESTRICT, null=True, blank=True)
    
    history = HistoricalRecords(excluded_fields=[], user_model=settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.nombre
    
class PuestoSuplente(models.Model):
    '''
        Puesto suplente en caso de estar deshabilitado el puesto
        o de vacaciones el usuario
    '''
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vigente = models.BooleanField(_('Estado'), default=True)
    
    puesto  = models.ForeignKey(Puesto, on_delete=models.CASCADE)
    suplente= models.ForeignKey(Puesto, on_delete=models.PROTECT, related_name='puesto_suplente')

    history = HistoricalRecords(excluded_fields=[], user_model=settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.suplente

class Vacaciones(models.Model):
    '''
        Programación de vacaciones por usuario
    '''
    ESTADOS = [
        ('P', 'Propuesto'),
        ('A', 'Autorizado'),
        ('C', 'Confirmado'),
        ('N', 'Anulado'),
    ]
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_inicio= models.DateField(_('Inicio'))
    fecha_fin   = models.DateField(_('Fin'))
    estado  = models.CharField(_('Estado'), choices=ESTADOS, default='P', max_length=1)
    # def_estado_display()

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    history = HistoricalRecords(excluded_fields=[], user_model=settings.AUTH_USER_MODEL)

    def __str__(self):
        return f'{self.fecha_inicio}-{self.fecha_fin}'

    def get_total_dias(self):
        return (self.fecha_fin-self.fecha_inicio).days if estado!='N' else 0

