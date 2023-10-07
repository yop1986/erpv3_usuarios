# ERPv3 - Usuarios

## Desarrollo

### Configuración del Ambiente

Es necesario instalar python, git y MariaDB. Posteriormente se utiliza pip 
(aplicativo incluido en las librerías de python) para instalar un ambiente 
virtual con el objetivo de aislar el proyecto de otras instalaciones.

Dentro de una carpeta creada específica para este proyecto (ERPv3) se 
procede a crear dicho ambiente virtual y el proyecto base.

    >pip install virtualenv
    >virtualenv .venv
    >.venv\Scripts\activate.bat

Se instala, dentro del ambiente virtual, django y su respectivo conector para 
la base de datos. 

    (venv) >pip install django mysqlclient

Se inicia el proyecto django y se descarga esta aplicación base con las 
configuraciones detalladas a continuación. Adicional es necesario crear 
la carpeta _static_ en la raiz del proyecto.

    (venv) ERPv3>django-admin startproject erpv3 .
    (venv) ERPv3>mkdir static

Dentro del direcotrio static es necesario crear un archivo de configuración 
general, dentro del cual se definiran alguna variables necesarias para el 
sistema bajo el formato: 

	[Encabezado]
	variable 	= valor

Contenido del archivo *__(venv) ERPv3/static/configuraciones.cfg__*:

	[sitio]
	#Información general del sitio
	nombre 		= ERPv3

Desde la consola de Git se procede a clonar este repositorio, en la raiz del 
proyecto.

    $ git clone https://github.com/yop1986/evp3_usuarios.git usuarios

Es necesario instalar las dependencias detalladas en el archivo 
_dependencias.txt_

	(venv) ERPv3>pip install -r usuarios/dependencias.txt

*dependencias creadas por medio del comando __pip freeze > dependencias.txt__*

#### Settings

Es necesario modificar el archivo **settings.py** del proyecto general con la
siguiente informacion:

	from django.contrib import messages
	from django.urls import reverse_lazy
	from django.utils.translation import gettext_lazy as _
	from pathlib import Path

	INSTALLED_APPS = [
		...
	    'crispy_forms',
	    'crispy_bootstrap5',
	    'usuarios',
	]

	TEMPLATES = [
	    {
	        ...
	        'DIRS': [BASE_DIR / 'templates/',],
	        ...
	    },
	]

	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': '<bbdd>',
	        'USER': '<usuario>',
	        'PASSWORD': '<contraseña>',
	        'HOST': '<ip|nombre del servidor>',
	        'PORT': '<puerto>',
	    }
	}

	LANGUAGE_CODE = 'es-gt'
	TIME_ZONE = 'America/Guatemala'
	USE_I18N = True
	USE_TZ = False

	STATIC_ROOT = BASE_DIR / "static"
	#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
	#STATICFILES_DIRS = [ BASE_DIR / "static", ]

	###
	### Servidor de correos
	###
	if DEBUG:
	    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
	else:
	    pass

	###
	### Variables Globales
	###
	# esta información para cada una de las apps instaladas
	MESSAGE_TAGS = {
	    messages.ERROR: "danger",
	}

	AUTH_USER_MODEL = 'usuarios.Usuario'
	LOGIN_URL = reverse_lazy('usuarios:login')
	LOGIN_REDIRECT_URL = reverse_lazy('usuarios:home')
	LOGOUT_REDIRECT_URL = reverse_lazy('usuarios:home')

	CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
	CRISPY_TEMPLATE_PACK = "bootstrap5"

	INFORMACION_APLICACIONES = {
	    '<nombre_app>': {
	        'nombre':       '<display>',
	        'descripcion':  _('<Descripción>'),
	        'url':          reverse_lazy('<namespace>:<nombre_url>'),
	        'imagen':       '<imagen>',
	    },
	}

#### Urls

Posterior a esta configuracion es necesario agregar las urls al proyecto base __< Base >/urls.py__

	from django.urls import path, include
    path('', include('usuarios.urls')),

#### Comandos adicionales de Django

	(venv) ERPv3> python manage.py check
	(venv) ERPv3> python manage.py makemigrations
	(venv) ERPv3> python manage.py migrate
	(venv) ERPv3> python manage.py createsuperuser
	(venv) ERPv3> python manage.py runserver <puerto>


## Producción

### Configuración del Ambiente


Cuando se instale en producción se debe generar otra clave y Debug = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--yy^#vtem@522nqsw4)69-ddtc_^xn&p#sl74$&jkw1^g9azy8'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True