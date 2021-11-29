"""
Django settings for Lead project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import json
import socket
import platform
import requests
from configparser import ConfigParser
from django.contrib.messages import constants as messages

config = ConfigParser()
config.read('config.ini')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['site']['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Dinamic Debug
DEBUG_PLATFORMS = ['Kevin-PC']
platform = platform.uname().node
if platform in DEBUG_PLATFORMS:
    DEBUG = True


# Get local ip address to be able to run the app in local network using runserver 0.0.0.0:8000
HOSTNAME = socket.gethostname()
LOCAL_IP = socket.gethostbyname(HOSTNAME).split(':')[0]

ALLOWED_HOSTS = ['selflink.link', 'www.selflink.link', 'localhost',
                 '127.0.0.1', '192.168.43.143']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_user_agents',
    'users.apps.UsersConfig',
    'leadfy.apps.LeadfyConfig',
    'subscriptions.apps.SubscriptionsConfig',
    'crispy_forms',
    'ckeditor',
    'ckeditor_uploader',
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    'allauth.socialaccount.providers.google',
    'django_cleanup.apps.CleanupConfig',
    # 'dbbackup',
    # 'django_unused_media',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'Lead.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'leadfy.context_processors.domain',
            ],
        },
    },
]

WSGI_APPLICATION = 'Lead.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE':  config['database']['ENGINE'],
            'NAME': config['database']['NAME'],
            'USER': config['database']['USER'],
            'PASSWORD': config['database']['PASSWORD'],
            'HOST': config['database']['HOST'],
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CKEDITOR_UPLOAD_PATH = 'uploads/'

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# LOGIN_REDIRECT_URL = 'home'
# LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config['email']['EMAIL_HOST']
EMAIL_HOST_PASSWORD = config['email']['EMAIL_HOST_PASSWORD']

PAYPAL_ENV = 'live'
PAYPAL_CID = config[PAYPAL_ENV]['CID']
PAYPAL_SECRET = config[PAYPAL_ENV]['SECRET']
PAYPAL_PRODUCT_ID = config[PAYPAL_ENV]['PRODUCT_ID']
PAYPAL_PLAN_ID = config[PAYPAL_ENV]['PLAN_ID']

GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_REDIRECT_URL = "home"
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''


ADMINS = [('Admin', EMAIL_HOST_USER)]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

MESSAGE_TAGS = {messages.ERROR: 'danger'}

# DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
# DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'backups')}

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    SITE_ID = 1

else:
    STATIC_ROOT = '/home/cristiangrey/leads/Lead/static'

    SITE_ID = 4

    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_REFERRER_POLICY = "strict-origin"

    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 86400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

try:
    _ = requests.head('http://google.com', timeout=5)
except requests.ConnectionError:
    if platform in DEBUG_PLATFORMS:
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
