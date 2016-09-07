# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['escapad.univ-lille3.fr', '127.0.0.1']

# SQLite conf
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
