import configparser

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.staticfiles.storage import staticfiles_storage

from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

#
# FUNCIONES GENERICAS
#
class Configuracion():
    def __init__(self, path=None, static=True, file='configuraciones.cfg'):
        '''
            Lee los archivos de configuración

            PARAMETROS
            path (string):  ruta base de la aplicacion donde se encuentra el archivo
            static (bool):  determina si se utilia la ruta defaul static de django
            file (string):  nombre del archivo de configuración (con su extension)
        '''
        self.config = configparser.RawConfigParser()
        
        if path is None:
            url = './' #ruta relativa; os.getcwd() #ruta completa;

        if static: 
            url += fr'{staticfiles_storage.url(file)}'
        else:
            url += fr'{file}'
        self.config.read_file(open(f'{url}', encoding='utf-8'))

    def get_value(self, pSection, pVariable):
        '''
            Devuelve un valor específico del archivo de configuración

            PARAMETROS
            pSection (string):  sección del archivo de donde se quiere obtener el valor
            pVariable (string): variable de la que se quiere obtener el valor
            
            RETURN
            Valor de la variable indicada
        '''
        return self.config[pSection][pVariable]

### ### ###
gConfiguracion = Configuracion()

class PersonalContextMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['general'] = {'nombre_sitio': gConfiguracion.get_value('sitio', 'nombre')}
        context['general']['menu_app'] = 'usuarios_menu.html'
        return context 

class PersonalTemplateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, PersonalContextMixin, TemplateView):
    pass

class PersonalFormView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, PersonalContextMixin, FormView):
    pass

class PersonalCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, PersonalContextMixin, CreateView):
    success_message = "Elemento creado correctamente"
    
class PersonalUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, PersonalContextMixin, UpdateView):
    success_message = "Elemento actualizado correctamente"
    
class PersonalListView(LoginRequiredMixin, PermissionRequiredMixin, PersonalContextMixin, ListView):
    pass

class PersonalDetailView(LoginRequiredMixin, PermissionRequiredMixin, PersonalContextMixin, DetailView):
    pass
    
class PersonalDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, PersonalContextMixin, DeleteView):
    success_message = "Elemento eliminado correctamente"