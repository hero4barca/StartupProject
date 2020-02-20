"""
Django settings for StartupProject project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/

import os
import socket# Import socket to read host name

"""

import os
import socket# Import socket to read host name

# If the host name starts with 'live', DJANGO_HOST = "production"
if socket.gethostname().startswith('live'):
    DJANGO_HOST = "production"
# Else if host name starts with 'test', set DJANGO_HOST = "test"
elif socket.gethostname().startswith('test'):
    DJANGO_HOST = "testing"
else:
# If host doesn't match, assume it's a development server, set DJANGO_HOST = "development"
    DJANGO_HOST = "development"




# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '&6j$jqjtv5g!_3-%v!7^^^8(nvkl*gjm2r$$!oa^sab@qc#8j('

#base on pythonanywhere example

SECRET_KEY = os.getenv("SECRET_KEY")



# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = ['www.mymarketwoman.com','hero4barca.pythonanywhere.com','localhost','127.0.0.1']

#Try and see the implication
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

#***********SSL SETTINGS*********
# -be sure adequate provision for HTTPS is made!!!!
SECURE_HSTS_SECONDS = 120
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_PRELOAD = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'GorceryDelivery.apps.GorcerydeliveryConfig',
    'django.contrib.humanize',
    'reportlab',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'GorceryDelivery.custommiddliware.ShopSessionsMiddleware',
]

ROOT_URLCONF = 'StartupProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'# to access MEDIA_URL in templates 'media'
            ],
        },
    },
]

WSGI_APPLICATION = 'StartupProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hero4barca$projectdb',
        'USER': 'hero4barca',                      # Not used with sqlite3.
        'PASSWORD': 'password@1',                  # Not used with sqlite3.
        'HOST': 'hero4barca.mysql.pythonanywhere-services.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATICFILES_DIRS = [
   # os.path.join(BASE_DIR, "static"),
#]

'''
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


'''



# Config for uploaded files
# to store item images

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#Session to expire at browser close
SESSION_EXPIRE_AT_BROWSER_CLOSE = True



# Define EMAIL_BACKEND variable for DJANGO_HOST
#if DJANGO_HOST == "production":
    # Output to SMTP server on DJANGO_HOST production

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = 'marketwomanph@zohomail.com'
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASS")
#'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' #os.getenv("SENDGRID_API_KEY")
EMAIL_PORT = 587



#
ADMINS = (('Administrator','marketwomanph@gmail.com'))
MANAGERS = ADMINS


# Define CACHES variable for DJANGO_HOST production and all other hosts
if DJANGO_HOST == "production":
   # Set cache
   CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT':'1800',
            }
        }
   CACHE_MIDDLEWARE_SECONDS = 1800
else:
   # No cache for all other hosts
   pass


#Celery
# Celery settings

#Broker'''
"""
BROKER_URL = 'amqp://guest:guest@localhost//'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULER ='djcelery.schedulers.DatabaseScheduler'
"""