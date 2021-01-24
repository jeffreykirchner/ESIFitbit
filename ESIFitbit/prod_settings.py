import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

STATIC_ROOT = '/home/esi/ESIFitbit/main/static'

ALLOWED_HOSTS = [os.environ['ALLOWED_HOST'],
                 'localhost',
                 '127.0.0.1']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

hostname = os.environ['DBHOST']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': hostname + ".postgres.database.azure.com",
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'],
        'OPTIONS': {'sslmode': 'require'},
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
           'filename': 'logs/debug.log',
           'maxBytes': 52428800,           #50 mb
           'backupCount' : 2,
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

#emails
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'   #log email to console
EMAIL_HOST = 'exchange.chapman.edu'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_USER_NAME = 'ESI Recruiter, Chapman University'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ['EMAIL_HOST_USER']

FITBIT_CLIENT_ID = os.environ['FITBIT_CLIENT_ID']
FITBIT_AUTHORIZATION = os.environ['FITBIT_AUTHORIZATION']
