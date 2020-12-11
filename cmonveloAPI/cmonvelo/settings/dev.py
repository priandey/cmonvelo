from . import *

DEBUG = True

SECRET_KEY = 's4a(dr#dh41_(2l891^*41wpfgerpg=maych#%h09$kc*$1-3&'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:63342",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cmonvelo',
        'USER': 'cmonvelouser',
        'PASSWORD': 'cmonvelo',
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ALLOWED_HOSTS = []