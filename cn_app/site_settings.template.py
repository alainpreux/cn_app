# SECURITY WARNING: don't run with debug turned on in production!
import os

DEBUG = True

ALLOWED_HOSTS = ['escapad.univ-lille3.fr', '127.0.0.1']

# SQLite conf
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3', # for production give absolute path when using sqlite3
    }
}

# Example with PostGreSQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'dbname',
#         'USER': 'dbuser',
#         'PASSWORD': 'dbpassword',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'agoodsecretkey'

# FIXME: logging maybe not suitable for production env (is it automatically redirect to log files ?)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'apps_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'escapad': {
            'handlers': ['apps_handler'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
