import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = 'main/static/'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split()

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': os.environ['DBHOST'] ,
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'],
        'OPTIONS': {'sslmode': 'prefer'},
    },
}


#logging, log both to console and to file log at the INFO level
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'info_format': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
            }
        },
    'handlers': {
        'console': {
            'level':'INFO',
            'class': 'logging.StreamHandler',
        },
       'logfile': {        
           'level':'INFO', 
           'class': 'logging.handlers.RotatingFileHandler',
           'filename': os.environ['LOG_LOCATION'],
           'maxBytes': 15728640,           #10 mb
           'backupCount' : 5,
           'formatter' : 'info_format',
           'delay': True,
       },
    },
    'loggers': {
        'django': {
            'handlers':['console','logfile'],
            'propagate': True,
            'level':'INFO',
        },
        'django.db.backends': {
            'handlers': ['console','logfile'],
            'level': 'INFO',
            'propagate': False,
        },
        'main': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',           
        },
        'django_cron': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',           
        },
    },
}

#tiny MCE
TINYMCE_DEFAULT_CONFIG = {
    "height" : 600,
    "menubar": False,
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code fullscreen insertdatetime media table paste code help wordcount",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}

#emails
FITBIT_CLIENT_ID = os.environ['FITBIT_CLIENT_ID']
FITBIT_AUTHORIZATION = os.environ['FITBIT_AUTHORIZATION']

PPMS_HOST = os.environ['PPMS_HOST']
PPMS_USER_NAME = os.environ['PPMS_USER_NAME']
PPMS_PASSWORD = os.environ['PPMS_PASSWORD']

#email service
EMAIL_MS_HOST = os.environ['EMAIL_MS_HOST']
EMAIL_MS_USER_NAME = os.environ['EMAIL_MS_USER_NAME']
EMAIL_MS_PASSWORD = os.environ['EMAIL_MS_PASSWORD']

#esit auth
ESI_AUTH_URL = 'https://esi-auth-dev.azurewebsites.net'
ESI_AUTH_ACCOUNT_URL = 'https://esi-auth-dev.azurewebsites.net/account/'
ESI_AUTH_PASSWORD_RESET_URL = 'https://esi-auth-dev.azurewebsites.net/password-reset/'

ESI_AUTH_USERNAME = 'fitbit_local'
ESI_AUTH_PASS = 'f4ac37gKgBy^je2Y'
ESI_AUTH_APP = 'Fitbit Local'
