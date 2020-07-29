"""
Django settings for the_care project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../")
sys.path.append("..")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8p*rr(@l=6u6vc%e167+h*5-9@42v45)5l6uhu8n0lnd4%up1q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imagekit',
    'Main',
    'Catalog',
    'Contacts',
    'Delivery',
    'News',
    'Payment',
    'Brands',
    'Basket',
    'Profile',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'the_care.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

WSGI_APPLICATION = 'the_care.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbvh9j72shni68',
        'USER': 'ctpgsekgklrode',
        'PASSWORD': '5538bf75a59b86696b02be9cb59ecfaef53f4c0b96f889ee3299de4eadb0a8c9',
        'HOST': 'ec2-54-247-72-30.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
        'CONN_MAX_AGE': None,
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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

# USE_I18N = True
#
# USE_L10N = True
#
# USE_TZ = True
USE_I18N = True

USE_L10N = True

USE_TZ = False

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

PIPELINE = {
    'STYLESHEETS': {
        'colors': {
            'source_filenames': (
              'css/animate.css',
              'css/bootstrap.css',
              'css/bootstrap.min.css',
              'css/noty.css',
              'css/slick.css',
              'css/slick-theme.css',
              'css/style.css'
            ),
            'output_filename': 'css/style.css',
            'extra_context': {
                'media': 'screen,projection',
            },
        },
    },
    'JAVASCRIPT': {
        'stats': {
            'source_filenames': (
              'js/bootstrap.js',
              'js/bootstrap.min.js',
              'js/main.js',
              'js/noty.js',
              'js/slick.min.js',
            ),
            'output_filename': 'js/main.js',
        }
    }
}

DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = 'ScXC5sD_X0AAAAAAAAAATKPrbFg-32dbxGIkw-DpExBnl-SRkIJLNG7COWtnQCFB'
DROPBOX_ROOT_PATH = '/the_care/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

CART_SESSION_ID = 'cart'
CART_USER = 'user'
LOGIN_URL = '/log_in'

PROD_LIST = []
TOP=''

PAY_LOGIN = 'thecare'
PAY_PASSWORD_1 = 'Yumbt46Uvps35bb8plFF'
PAY_PASSWORD_2 = 'tz8VOaOG9ZSFLfk5H23e'
# PAY_TEST_PASSWORD_1 = 'ldy1yH3vsf049uwvpRpJ'
PAY_TEST_PASSWORD_1 = 'test_pass_1'
PAY_TEST_PASSWORD_2 = 'V8nNBsOSEW3a2pvXc71J'

MC_CLIENT_ID='836169265342'
MC_CLIENT_SECRET='da69bffa1356fe682f1cf4e00241ecc91dd87e75f2a1bcec33'

EMAIL_HOST = 'smtp-pulse.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = "avdeenkoaleksey@gmail.com"
EMAIL_HOST_PASSWORD = "YRtMP4Dso4R"
EMAIL_USE_SSL = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_REST_API_ID='f25ed79d241c819cbab226a651ad9187'
EMAIL_REST_API_SECRET='9aff1c233fa1de995cf612d13a7f6c29'