import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration



if os.environ.get("APP_ENABLE_PROFILING", "").lower() in {'1', 'yes', 'true'}:
    print('Profiling middleware: ENABLED')
    experiments = {
        "profiles_sample_rate": 1.0,
        "profiler_mode": "sleep",
    }
else:
    print('Profiling middleware: DISABLED')
    experiments = {}

sentry_sdk.init(
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    _experiments=experiments,
    # debug=True,
)

DEBUG = True

SECRET_KEY = '_7mb6#v4yf@qhc(r(zbyh&amp;z_iby-na*7wz&amp;-v6pohsul-d#y5f'
ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + os.environ['DJANGO_DB'], # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'hello_world',           # Or path to database file if using sqlite3.
        'USER': 'benchmarkdbuser',       # Not used with sqlite3.
        'PASSWORD': 'benchmarkdbpass',   # Not used with sqlite3.
        'HOST': '127.0.0.1',             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                  # Set to empty string for default. Not used with sqlite3.
        'CONN_MAX_AGE': 30,
    }
}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False
USE_TZ = False

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = ()
MIDDLEWARE = []

ROOT_URLCONF = 'hello.urls'
WSGI_APPLICATION = 'hello.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {},
    },
]

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'world',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {},
    'loggers': {},

}

ALLOWED_HOSTS = ['*']
