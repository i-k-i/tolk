"""
Django settings for tolk project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '22s@*=z#048cy0ml#c8j2&b9!953*jg+5t(s$*9-wg-%c3au!k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'projector',
    'taggit',
    'south',
    'loginsys',
##    'filer',
##    'easy_thumbnails',
##    'django.contrib.comments',
##    'mptt',
##    'comments',
##    'threadedcomments',
##    'django.contrib.comments',
##    'nicedit',
    'redactor',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tolk.urls'

WSGI_APPLICATION = 'tolk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
## static
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
#    os.path.join(BASE_DIR, 'redactor', 'static', 'redactor'),

)
##

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'

SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}

THUMBNAIL_HIGH_RESOLUTION = True

#MEDIA_ROOT ='/home/stik/tolk/media/'

#MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = 'media/uploads/'
#REDACTOR_UPLOAD = 'uploads/'

REDACTOR_UPLOAD_HANDLER = 'redactor.handlers.DateDirectoryUploader'
