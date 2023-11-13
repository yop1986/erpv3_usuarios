from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetConfirmView, 
    PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeView)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from .models import Usuario
from .forms import CustomUserCreationForm, CustomUserUpdateForm, PerfilForm

from .personal_views import (PersonalTemplateView, PersonalListView, PersonalFormView, 
    PersonalUpdateView)
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
            'nombre_sitio': sitio
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



class UsuarioLoginView(LoginView):
    template_name = "usuarios/login.html"
    extra_context = {
        'title': _('Página de ingreso'),
        'opciones': {
            'submit': _('Ingresar'),
            'reset': _('He olvidado la contraseña'),
        },
    }

    def get_context_data(self, *args, **kwargs):
        context = super(UsuarioLoginView, self).get_context_data(*args, **kwargs)
        context['general'] = {'nombre_sitio': gConfiguracion.get_value('sitio', 'nombre')}
        return context


class UsuarioLogoutView(LogoutView):
    pass


class UsuarioPasswordResetView(PasswordResetView):
    template_name = "usuarios/password_reset_form.html"
    subject_template_name = "usuarios/password_reset_subject.txt"
    email_template_name = "usuarios/password_reset_email.html"
    success_url = reverse_lazy("usuarios:password_reset_done")
    extra_context = {
        'opciones': {
            'submit': _('Soliciar'),
        },
    }

    def get_context_data(self):
        context = super(UsuarioPasswordResetView, self).get_context_data()
        context['general'] = {'nombre_sitio': gConfiguracion.get_value('sitio', 'nombre')}
        return context


class UsuarioPasswordResetDoneView(PasswordResetDoneView):
    template_name = "usuarios/password_reset_done.html"


class UsuarioPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "usuarios/password_reset_confirm.html"
    success_url = reverse_lazy("usuarios:password_reset_complete")
    extra_context ={
        'opciones': {
            'submit': _('Cambiar')
        },
    }

    def get_context_data(self):
        context = super(UsuarioPasswordResetConfirmView, self).get_context_data()
        context['general'] = {'nombre_sitio': gConfiguracion.get_value('sitio', 'nombre')}
        return context


class UsuarioPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "usuarios/password_reset_complete.html"
    extra_context ={
        'opciones': {
            'ingresar': _('Ingresar')
        },
    }

    def get_context_data(self):
        context = super(UsuarioPasswordResetCompleteView, self).get_context_data()
        context['general'] = {'nombre_sitio': gConfiguracion.get_value('sitio', 'nombre')}
        return context


class UsuarioPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'usuarios/password_change_form.html'
    success_message = 'Contraseña cambiada correctamente'
    success_url = reverse_lazy('usuarios:perfil')
    extra_context = {
        'opciones': {
            'submit': _('Cambiar'),
        },
    }

    def get_context_data(self):
        context = super(UsuarioPasswordChangeView, self).get_context_data()
        context['general'] = {'nombre_sitio': gConfiguracion.get_value('sitio', 'nombre')}
        return context


class PerfilTemplateView(PersonalTemplateView):
    '''
        Muestra la información del perfil de usuario
    '''
    template_name = 'usuarios/perfil.html'
    permission_required = 'usuarios.view_perfil'
    extra_context ={
        'title': _('Perfil'),
    }

    def get_context_data(self):
        context = super(PerfilTemplateView, self).get_context_data()
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
            'editar': _('Editar'),
        },
    }

    def get_queryset(self):
        valor_busqueda = self.request.GET.get('valor')
        if valor_busqueda:
            if 'mail:' in valor_busqueda:
                return Usuario.objects.filter(email__icontains=valor_busqueda[5:]).order_by('email')
            elif 'name:' in valor_busqueda:
                return Usuario.objects.filter(
                    busqueda_nombres(
                        campos=['first_name__icontains', 'last_name__icontains'], 
                        valores=valor_busqueda[5:].split(' ')),
                    ).order_by('first_name', 'last_name')
            else:
                return Usuario.objects.filter(username__icontains=valor_busqueda).order_by('username')
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
