import os
import json

from django.core.exceptions import ImproperlyConfigured

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if os.path.exists(os.path.join(BASE_DIR, "envs.json")):
    with open(os.path.join(BASE_DIR, "envs.json")) as f:
        envs = json.loads(f.read())

    def get_env(setting, envs):
        try:
            return envs[setting]
        except KeyError:
            error_msg = "set env var error at {}".format(setting)
            raise ImproperlyConfigured(error_msg)

    FACEBOOK_KEY = get_env("FACEBOOK_KEY", envs)
    FACEBOOK_SECRET = get_env("FACEBOOK_SECRET", envs)
    GOOGLE_KEY = get_env("GOOGLE_KEY", envs)
    GOOGLE_SECRET = get_env("GOOGLE_SECRET", envs)
    PAYPAL_ID = get_env("PAYPAL_ID", envs)

    GMAIL_ID = get_env("GMAIL_ID", envs)
    GMAIL_PW = get_env("GMAIL_PW", envs)

else:
    FACEBOOK_KEY = os.environ["FACEBOOK_KEY"]
    FACEBOOK_SECRET = os.environ["FACEBOOK_SECRET"]
    GOOGLE_KEY = os.environ["GOOGLE_KEY"]
    GOOGLE_SECRET = os.environ["GOOGLE_SECRET"]
    PAYPAL_ID = os.environ["PAYPAL_ID"]
    GMAIL_ID = os.environ["GMAIL_ID"]
    GMAIL_PW = os.environ["GMAIL_PW"]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'awl40xu110@48pc#0ej)aeqkbs)f8&a)946oalt*d2(f-^&=6o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ckeditor for admin
    'ckeditor',
    'ckeditor_uploader',
    # My Apps
    'goods',
    # Social Login
    'social.apps.django_app.default',
    # Cart and Google Address
    'carton',
    'address',
    # Paypal
    'paypal.standard.ipn',
    # django health check
    'health_check',
    'health_check_celery3',
    'health_check_db',
    'health_check_cache',
    'health_check_storage',
    # Celery
    'djcelery',
    #DJDT
    'debug_toolbar',
]

#CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #DJDT
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'irkshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'irkshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# Social Login
AUTHENTICATION_BACKENDS = [
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_REDIRECT_URL='/'

'''
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)
'''

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# SocialLogin: Facebook
SOCIAL_AUTH_FACEBOOK_KEY = FACEBOOK_KEY
SOCIAL_AUTH_FACEBOOK_SECRET = FACEBOOK_SECRET
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email, age_range'
}

# SocialLogin: Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GOOGLE_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_SECRET
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

LANGUAGES = (
    ('en-us', _('English')),
    ('ko-kr', _('Korean')),
)

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static_deploy/')

# Media/Upload files
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# CKEDITOR Settings
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ]
    },
}

# Shopping Cart

CART_PRODUCT_MODEL = 'goods.models.Goods'

PAYPAL_TEST = True

# DJDT
INTERNAL_IPS = '127.0.0.1'