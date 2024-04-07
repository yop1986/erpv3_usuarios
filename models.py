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


### CATALOGOS ###
class Departamento(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo      = models.CharField(_('Códgio'), max_length=2)
    descripcion = models.CharField(_('Departamento'), max_length=30)
    
    def __str__(self):
        return self.descripcion

class Municipio(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo      = models.CharField(_('Códgio'), max_length=4)
    descripcion = models.CharField(_('Municipio'), max_length=60)
    
    departamento= models.ForeignKey(Departamento, on_delete=models.RESTRICT)

    def __str__(self):
        return self.descripcion

    def get_ubicacion_completa(self):
        return f'{self.departamento}, {self.descripcion}'



