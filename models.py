import uuid
import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

class Usuario(AbstractUser):
    '''
        Información propia del usuario, asociada a la cuenta y accesos
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name_description = _('Nombre Completo')
    is_active_description = _('Estado')

    class Meta:
        pass
        #permissions = [
        #    ('create_usuario', 'Permite la creación de usuarios'),
        #]

class Perfil(models.Model):
    '''
        Información adicional del usuario
    '''
    telefono    = models.CharField(_('Telefono'), max_length=12, blank=True)
    celular     = models.CharField(_('Celular'), max_length=12, blank=True)
    dpi         = models.CharField(_('DPI'), max_length=13, blank=True)
    nit         = models.CharField(_('Nit'), max_length=10, blank=True)
    fecha_nacimiento = models.DateField(_('Fecha de nacimiento'), null=True, blank=True)
    usuario     = models.OneToOneField(Usuario, on_delete = models.CASCADE)

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

