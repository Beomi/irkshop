import os
import json

from django.core.exceptions import ImproperlyConfigured

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = []

# Env for dev / deploy
def get_env(setting, envs):
    try:
        return envs[setting]
    except KeyError:
        error_msg = "set env var error at {}".format(setting)
        raise ImproperlyConfigured(error_msg)

DEV_ENVS = os.path.join(BASE_DIR, "envs_dev.json")
DEPLOY_ENVS = os.path.join(BASE_DIR, "envs.json")

if os.path.exists(DEV_ENVS): # Develop Env
    f = open(DEV_ENVS)
elif os.path.exists(DEPLOY_ENVS): # Deploy Env
    f = open(DEPLOY_ENVS)
    DEBUG = False
else:
    f = None
    DEBUG = False

if f is None: # System environ
    try:
        FACEBOOK_KEY = os.environ.get('FACEBOOK_KEY')
        FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET')
        GOOGLE_KEY = os.environ.get('GOOGLE_KEY')
        GOOGLE_SECRET = os.environ.get('GOOGLE_SECRET')
        PAYPAL_ID = os.environ.get('PAYPAL_ID')
        GMAIL_ID = os.environ.get('GMAIL_ID')
        GMAIL_PW = os.environ.get('GMAIL_PW')
        DB_NAME = os.environ.get('DB_NAME')
        DB_USER = os.environ.get('DB_USER')
        DB_PW = os.environ.get('DB_PW')
        DB_HOST = os.environ.get('DB_HOST')
        DB_PORT = os.environ.get('DB_PORT')
    except KeyError as error_msg:
        raise ImproperlyConfigured(error_msg)
else: # JSON env
    envs = json.loads(f.read())
    FACEBOOK_KEY = get_env('FACEBOOK_KEY', envs)
    FACEBOOK_SECRET = get_env('FACEBOOK_SECRET', envs)
    GOOGLE_KEY = get_env('GOOGLE_KEY', envs)
    GOOGLE_SECRET = get_env('GOOGLE_SECRET', envs)
    PAYPAL_ID = get_env('PAYPAL_ID', envs)
    GMAIL_ID = get_env('GMAIL_ID', envs)
    GMAIL_PW = get_env('GMAIL_PW', envs)
    DB_NAME = get_env('DB_NAME', envs)
    DB_USER = get_env('DB_USER', envs)
    DB_PW = get_env('DB_PW', envs)
    DB_HOST = get_env('DB_HOST', envs)
    DB_PORT = get_env('DB_PORT', envs)

# Heroku or Not
if os.environ.get('HEROKU', False): # if Heroku
    HEROKU = True
    DEBUG = False
    ALLOWED_HOSTS += [os.environ.get('HEROKU_DOMAIN', '*')]
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
else: # or Not
    HEROKU = False
    DEBUG = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'awl40xu110@48pc#0ej)aeqkbs)f8&a)946oalt*d2(f-^&=6o'

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
    # Email User
    'custom_user',
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
if DB_NAME and (not DEBUG): # Deploy, RDS like.    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PW,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
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

# Email User

AUTH_USER_MODEL = 'custom_user.EmailUser'

# Social Login
AUTHENTICATION_BACKENDS = [
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_REDIRECT_URL='/'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

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


# Heroku DB
if HEROKU:
    # Update database configuration with $DATABASE_URL.
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)
