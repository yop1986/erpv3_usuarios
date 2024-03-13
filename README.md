# ERPv3 - Usuarios

## Desarrollo

### Configuración del Ambiente

Es necesario instalar python, git y MariaDB. Posteriormente se utiliza pip 
(aplicativo incluido en las librerías de python) para instalar un ambiente 
virtual con el objetivo de aislar el proyecto de otras instalaciones.

Dentro de una carpeta creada específica para este proyecto (ERPv3) se 
procede a crear dicho ambiente virtual y el proyecto base.

    >pip install virtualenv pip-review
    >virtualenv .venv
    >.venv\Scripts\activate.bat

Dentro de la carpeta creada para el poryecto, se procede a utilizar Git para 
clonar este repositorio (base) para todos los aplicativos del ERP. 

	$git clone https://github.com/yop1986/evp3_usuarios.git usuarios

Se instalan todas las dependencias necesarias para estos proyectos incluidas
en el repositorio y se actualiza.

	>pip install -r usuarios\dependencias.txt
	>pip-review # Muestra paquetes desactualizados
	>pip-review --auto # Instala todas las actualizaciones
	>pip-review --interactive # Pregunta cada paquete que se desee actualizar

*django ckeditor https://pypi.org/project/django-ckeditor-5//*
*dependencias creadas por medio del comando __pip freeze > dependencias.txt__*

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
	    'django_ckeditor_5',
	    
	    'usuarios',
	]

    MIDDLEWARE = [
        ...
        'simple_history.middleware.HistoryRequestMiddleware',
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

	STATIC_URL = '/static/'
	#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
	STATIC_ROOT = BASE_DIR / "static"
	#STATICFILES_DIRS = [ BASE_DIR / "static", ]

	MEDIA_URL = '/media/'
	#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
	MEDIA_ROOT = BASE_DIR / "media"


	###
	### Servidor de correos
	###
	if DEBUG:
	    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
	    #Para guardar los correos de prueba en una ubicacion (hay que crear la ruta indicada)
	    #EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
	    #EMAIL_FILE_PATH = 'C://ubicacion//correos//' # ruta para genrear archivos
	else:
	    EMAIL_USE_TLS = False
	    EMAIL_USE_SSL = False
	    EMAIL_HOST = '<ip | nombre>'
	    EMAIL_PORT = <puerto>

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

	customColorPalette = [
	        {
	            'color': 'hsl(4, 90%, 58%)',
	            'label': 'Red'
	        },
	        {
	            'color': 'hsl(340, 82%, 52%)',
	            'label': 'Pink'
	        },
	        {
	            'color': 'hsl(291, 64%, 42%)',
	            'label': 'Purple'
	        },
	        {
	            'color': 'hsl(262, 52%, 47%)',
	            'label': 'Deep Purple'
	        },
	        {
	            'color': 'hsl(231, 48%, 48%)',
	            'label': 'Indigo'
	        },
	        {
	            'color': 'hsl(207, 90%, 54%)',
	            'label': 'Blue'
	        },
	    ]

	  CKEDITOR_5_CONFIGS = {
	    'default': {
	        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
	                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

	    },
	    'extends': {
	        'blockToolbar': [
	            'paragraph', 'heading1', 'heading2', 'heading3',
	            '|',
	            'bulletedList', 'numberedList',
	            '|',
	            'blockQuote',
	        ],
	        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
	        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
	                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
	                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
	                    'insertTable',],
	        'image': {
	            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
	                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
	            'styles': [
	                'full',
	                'side',
	                'alignLeft',
	                'alignRight',
	                'alignCenter',
	            ]

	        },
	        'table': {
	            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
	            'tableProperties', 'tableCellProperties' ],
	            'tableProperties': {
	                'borderColors': customColorPalette,
	                'backgroundColors': customColorPalette
	            },
	            'tableCellProperties': {
	                'borderColors': customColorPalette,
	                'backgroundColors': customColorPalette
	            }
	        },
	        'heading' : {
	            'options': [
	                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
	                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
	                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
	                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
	            ]
	        }
	    },
	    'list': {
	        'properties': {
	            'styles': 'true',
	            'startIndex': 'true',
	            'reversed': 'true',
	        }
	    }
	}

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
	
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
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


# Problemas con PIP
## Configuracion de proxy

Agregar el proxy: 
	pip config --global set global.proxy=<usuario>:<contrañeña>@<direraccion>:<puerto>

Quitar el proxy
	pip config --global unset global.proxy

## Configuracion de sitio de paquetes seguros

Cuando se intenta una instalación de software de los repositorios oficiales, se muestra el mensaje

	WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:992)'))': /simple/websocket/

Una opcion para solvertar este problema es agregar a sitios seguros de pip el origen de las aplicaciones. Esto se hace modificando el archivo pip.ini, usualmente en alguna de estas rutas:

- C:\ProgramData\pip\pip.ini
- %appdata%\Roaming\pip

Y se agrega esto en el archivo:

	[global]
	trusted-host = pypi.python.org
    	           pypi.org
        	       files.pythonhosted.org
