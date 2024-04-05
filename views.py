import operator
from functools import reduce

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetConfirmView, 
    PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeView)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from .models import Usuario, Perfil
from .forms import CustomUserCreationForm, CustomUserUpdateForm, PerfilForm

from .personal_views import (PersonalContextMixin, PersonalTemplateView, PersonalListView, 
    PersonalFormView, PersonalUpdateView)
from .personal_views import Configuracion
#
# LECTURA DE ARCHIVO DE CONFIGURACIÓN
#

gConfiguracion = Configuracion()

def app_installed(apps):
    '''
        Valida si la aplicacion esta instalada
    '''
    installed = list()
    for app in apps:
        if app in settings.INSTALLED_APPS:
            installed.append(apps[app])
    return installed

#
# FUNCIONES Y VISTAS GENERICAS
#    

def home(request):
    sitio  = gConfiguracion.get_value('sitio', 'nombre')
    info = {
        'general': {
            'nombre_sitio': sitio,
            'menu_app': 'usuarios_menu.html',
        },
        'contenido': {
            'title': _(sitio),
            'h1': _('Aplicaciones instaladas'),
        },
        'apps': app_installed(settings.INFORMACION_APLICACIONES),
        'opciones': {
            'ir': _('Ir'),
        },
    }
    return render(request, 'home.html', info)


class UsuarioLoginView(LoginView, PersonalContextMixin):
    template_name = "usuarios/login.html"
    extra_context = {
        'title': _('Página de ingreso'),
        'opciones': {
            'submit': _('Ingresar'),
            'reset': _('He olvidado la contraseña'),
        },
    }

class UsuarioLogoutView(LogoutView):
    pass

# Inicia TODAS las acciones del reset
class UsuarioPasswordResetView(PasswordResetView, PersonalContextMixin):
    template_name = "usuarios/password_reset_form.html"
    subject_template_name = "usuarios/password_reset_subject.txt"
    email_template_name = "usuarios/password_reset_email.html"
    success_url = reverse_lazy("usuarios:password_reset_done")
    extra_context = {
        'opciones': {
            'submit': _('Soliciar'),
        },
    }

class UsuarioPasswordResetDoneView(PasswordResetDoneView, PersonalContextMixin):
    template_name = "usuarios/password_reset_done.html"

class UsuarioPasswordResetConfirmView(PasswordResetConfirmView, PersonalContextMixin):
    template_name = "usuarios/password_reset_confirm.html"
    success_url = reverse_lazy("usuarios:password_reset_complete")
    extra_context ={
        'opciones': {
            'submit': _('Cambiar')
        },
    }

class UsuarioPasswordResetCompleteView(PasswordResetCompleteView, PersonalContextMixin):
    template_name = "usuarios/password_reset_complete.html"
    extra_context ={
        'opciones': {
            'ingresar': _('Ingresar')
        },
    }
# Finaliza TODAS las acciones del reset

class UsuarioPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView, PersonalContextMixin):
    template_name = 'template/forms.html'
    success_message = 'Contraseña cambiada correctamente'
    success_url = reverse_lazy('usuarios:perfil')
    extra_context = {
        'opciones': {
            'submit': _('Cambiar'),
        },
    }

class PerfilTemplateView(PersonalTemplateView):
    '''
        Muestra la información del perfil de usuario
    '''
    template_name = 'usuarios/perfil.html'
    permission_required = 'usuarios.view_perfil'
    extra_context ={
        'title': _('Perfil'),
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object'] = Usuario.objects.get(pk=self.request.user.id)
        return context

class PerfilUpdateView(PersonalUpdateView):
    '''
        Actualización del usuario que está logueado actualmente
        (Unicamente actualiza el propio perfil)
    '''
    permission_required = 'usuarios.change_perfil'
    model = Usuario
    fields = ['first_name', 'last_name', 'email']
    success_message = 'Usuario actualizado correctamente'
    success_url = reverse_lazy('usuarios:perfil')
    extra_context ={
        'title': _('Actualización de datos'),
        'opciones': {
            'submit': _('Modificar'),
        },
    }

    def get_object(self):
        return Usuario.objects.get(pk=self.request.user.id)

    def get_context_data(self, *args, **kwargs):
        context = super(PerfilUpdateView, self).get_context_data(*args, **kwargs)
        context['aditional_form'] = PerfilForm(instance=self.request.user.perfil)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        aditional_form = PerfilForm(request.POST or None, instance=self.object.perfil)

        if form.is_valid() and aditional_form.is_valid():
            form.save()
            aditional_form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(PerfilUpdateView, self).form_invalid(form)

class UsuarioCreateView(PersonalFormView):
    template_name = 'usuarios/usuario_form.html'
    permission_required = 'usuarios.add_usuario'
    form_class = CustomUserCreationForm
    success_message = _('Usuario creado correctamente')
    success_url = reverse_lazy('usuarios:home')
    extra_context ={
        'title': _('Creación de usuario'),
        'opciones': {
            'submit': _('Crear'),
        },
    }

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super(UsuarioCreateView, self).form_valid(form)

class UsuarioListView(PersonalListView):
    '''
        Lista de usuarios registrados en la aplicacion
    '''
    permission_required = 'usuarios.view_usuario'
    model = Usuario
    ordering = ('username')
    paginate_by = 12
    extra_context ={
        'title': _('Lista de usuarios'),
        'opciones': {
            'etiqueta': _('Opciones'),
            'ver': _('Ver'),
            'editar': _('Editar'),
        },
    }

    def get_queryset(self):
        valor_busqueda = self.request.GET.get('valor')
        if valor_busqueda:
            if 'mail:' in valor_busqueda:
                return Usuario.objects.filter(email__icontains=valor_busqueda[5:]).order_by('username')
            elif 'name:' in valor_busqueda:
                valores = valor_busqueda[5:].split(' ')
                query_filter = reduce(operator.or_, (Q(first_name__icontains=f'{valor}')|Q(last_name__icontains=f'{valor}') for valor in valores))
                return Usuario.objects.filter(query_filter).order_by('username')
            else:
                return Usuario.objects.filter(username__icontains = valor_busqueda).order_by('username')
        else:
            return super(UsuarioListView, self).get_queryset()

class UsuarioUpdateView(PersonalUpdateView):
    '''
        Actualización de usuarios terceros
        Como una funcion administrativa
    '''
    template_name = 'usuarios/usuario_form.html'
    permission_required = 'usuarios.change_usuario'
    model = Usuario
    form_class = CustomUserUpdateForm
    success_message = _('Usuario actualizado correctamente')
    success_url = reverse_lazy('usuarios:listar')
    extra_context ={
        'title': _('Actualizar Usuarios'),
        'opciones': {
            'submit': _('Modificar'),
        },
    }

    def get_context_data(self, *args, **kwargs):
        context = super(UsuarioUpdateView, self).get_context_data(*args, **kwargs)
        context['aditional_form'] = PerfilForm(instance=self.object.perfil)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        aditional_form = PerfilForm(request.POST, instance=self.object.perfil)

        if form.is_valid() and aditional_form.is_valid():
            form.save()
            aditional_form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(UsuarioUpdateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('usuarios:detail_user', kwargs={'pk': self.get_object().id})

class UsuarioDetailView(PersonalTemplateView):
    '''
        Muestra la información del perfil de cualqueir usuario
    '''
    template_name = 'template/templatedetail_multiple_objects.html'
    permission_required = 'usuarios.view_usuario'
    extra_context ={
        'title': _('Usuario'),
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        usuario = Usuario.objects.get(pk=kwargs['pk'])
        context['objects'] = [
            {
               'object': usuario,
                'campos':{
                    'lista': ['email', ]
                },
                'campos_extra': [
                    {'nombre': _('Estado'), 'funcion': 'get_estado'},
                    {'nombre': _('Grupos'), 'ul_lista': usuario.get_grupos()},
                ]
            },
            {
               'object': Perfil.objects.get(usuario = usuario),
                'campos':{
                    'lista': ['telefono', 'celular', 'dpi', 'nit', 'fecha_nacimiento', ]
                },
                'campos_extra': [
                    {'nombre': _('Edad'), 'funcion': 'get_edad'},
                ]
            },
        ]
        context['opciones'] = {
            'display':  _('Opciones'),
            'update':   _('Editar'),
            'update_url': reverse_lazy('usuarios:actualizar', kwargs={'pk': kwargs['pk']}),
            'update_img': 'usuario_update.png',
            'update_perm': self.request.user.has_perm('usuarios.change_usuario'),
        }
        context['grupos'] = { 'nombre': _('Grupos'), 'ul': usuario.get_grupos() }
        
        return context