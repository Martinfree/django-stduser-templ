import datetime
import os
import sys
import logging
import logging.config
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#-+2%cfp05=)8q*u1s2itkffi$i^@ir5@bv%!9g3irbfi_)2h5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Update in prod it
ALLOWED_HOSTS = ['localhost',
                 '0.0.0.0',
                 '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django_nose',

    'djangotoolbox',

    'apps.authentication',
    'apps.utils',
    'django_crontab',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
AUTH_USER_MODEL = 'authentication.StdUser'
# email confirm configuration

ACCOUNT_EMAIL_REQUIRED = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'cecs.department.noreply@gmail.com'
EMAIL_HOST_PASSWORD = 'WWwf6Max'

VERIFICATION_URL = 'verify'
RECOVER_URL = 'completerecover'
VERIFICATION_CODE_EXPIRED = 1
RECOVER_CODE_EXPIRED = 1

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
        )
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'apps/utils/templates'),
            os.path.join(BASE_DIR, 'apps/mailing/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],

        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgresql',
        'USER': 'admin',
        'PASSWORD': 'Admin123!',
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_database',
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS':{
            'min_length':8,
            }

    },

    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

    {
        'NAME': 'apps.authentication.validators.SymbolPasswordValidator',

    },

    {
        'NAME': 'apps.authentication.validators.CharPasswordValidator',

    },

    {
        'NAME': 'apps.authentication.validators.UpPasswordValidator',

    },
    {
        'NAME': 'apps.authentication.validators.LowPasswordValidator',

    },
]

# settings for rest framework
REST_FRAMEWORK = {
        'EXCEPTION_HANDLER': 'apps.utils.exceptions.exception_handler',
#JWT
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
#Permissions
    'DEFAULT_PERMISSION_CLASSES': (
        'apps.utils.permissions.IsAdminUser',
        'apps.utils.permissions.IsModeratorUser',
        'apps.utils.permissions.IsAuthenticated',
        'apps.utils.permissions.DisablePermission',
    ),
}

SIMPLE_JWT = {
    'AUTH_HEADHER_TYPE': 'Bearer',
    'USER_ID_FIELD': 'id',
    'PAYLOAD_ID_FIELD': 'user_id',
    
    'TOKEN_BACKEND': 'rest_framework_simplejwt.backends.TokenBackend',
    
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'
REST_USE_JWT = True

# providers settings
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender', 
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': True,
        'VERSION': 'v2.12',
    },
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

# allauth user relation
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_ADAPTER = 'authentication.adapter.UserSocialAccountAdapter'
# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# redirect urls
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL ='/accounts/login/'

# admins to send
ADMINS =[]
MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    #standart formatters
    'formatters': {
        'STANDART': {
            'style': '{',
            'format': '[ {levelname} at {asctime}]\n {message} ' ,},
        },
    #standart handlers
    'handlers': {

            #stdout
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'STANDART',
                'stream': sys.stdout,},

            #send mail about crit error
            'mail_admins': {
                'class': 'django.utils.log.AdminEmailHandler',
                'level': 'CRITICAL',
                'include_html': True,
                },

            #warning file handler
            'warning_stream': {
                'level': 'WARNING',
                'formatter': 'STANDART',
                'class': 'logging.FileHandler',
                'filename': 'logs/warning.log',},

            #error file handler
            'error_stream': {
                'level': 'ERROR',
                'formatter': 'STANDART',
                'class': 'logging.FileHandler',
                'filename': 'logs/error.log',},

            },

            'loggers': {
                #default logger for all
                '': {
            'handlers': ['warning_stream','error_stream','console','mail_admins'],
            'level': 'DEBUG',
            'propagate': True,},
                #main logger
                'django': {
                    'handlers': ['warning_stream','error_stream','console','mail_admins'],
                    'propagate': True,},
        },
}

SITE_ID = 2

logging.config.dictConfig(LOGGING)
