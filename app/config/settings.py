"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG = int(os.environ.get('DEBUG', default=0))

if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    # ALLOWED_HOSTS = [os.environ.get("DOMAIN")]
    ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # 自作
    'wooys.apps.WooysConfig',
    'accounts.apps.AccountsConfig',

    # install
    'storages',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_ses',
    'widget_tweaks',
    'imagekit',


    # default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # テンプレートを置く場所
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DATABASE_DB', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('DATABASE_USER', 'user'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'password'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
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

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# S3 設定
USE_S3 = os.getenv('USE_S3') == 'TRUE'

if USE_S3:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = '%s.s3-ap-northeast-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'
    AWS_DEFAULT_ACL = None
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'config.storage_backends.StaticStorage'

    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, 'media')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage'
else:
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    # MEDIA_URL : メディアファイル公開時のURLのプレフィクス。url=http://アプリのドメイン+MEDIA_URL+メディアファイル名
    MEDIA_URL = '/media/'
    # MEDIA_ROOT : サーバから見たメディアルートの絶対パス. プロジェクトトップディレクトリ/media
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


APPEND_SLASH = False


# SES設定
AWS_SES_ACCESS_KEY_ID = os.environ.get("AWS_SES_ACCESS_KEY_ID")
AWS_SES_SECRET_ACCESS_KEY = os.environ.get("AWS_SES_SECRET_ACCESS_KEY")
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")


# ユーザーモデル
AUTH_USER_MODEL = "accounts.CustomUser"

# auth
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    # 一般（メールアドレス）
    'allauth.account.auth_backends.AuthenticationBackend',
    # 管理者（ユーザーネーム）
    'django.contrib.auth.backends.ModelBackend',
)
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # 認証方法をメールアドレスにする
ACCOUNT_USERNAME_REQUIRED = True  # ユーザー名を要求する
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # メールを送信する
DEFAULT_FROM_EMAIL = SERVER_EMAIL = "admin@"+os.environ.get("DOMAIN")
ACCOUNT_EMAIL_REQUIRED = True  # メールアドレスを要求する
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True  # サインインメール確認後自動でログイン
LOGIN_REDIRECT_URL = 'wooys:index'
ACCOUNT_LOGOUT_REDIRECT_URL = 'wooys:index'
ACCOUNT_LOGOUT_ON_GET = True  # ログアウトリンク一発でログアウト


# メッセージ
MESSAGE_TAGS = {
    messages.ERROR: "alert alert-danger",
    messages.WARNING: "alert alert-warning",
    messages.SUCCESS: "alert alert-success",
    messages.INFO: "alert alert-info",
}


# ロガー設定
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        # ハンドラ
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'dev',
            }
        },
        # ロガー
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            # 追加
            'wooys': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },

        # フォーマッター
        'formatters': {
            'dev': {
                'format': '\t'.join([
                    '%(asctime)s',
                    '[%(levelname)s]',
                    '%(pathname)s(Line:%(lineno)d)',
                    '%(message)s'
                ])
            }
        },
    }
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        # ロガー
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'INFO',
            },
            # 追加
            'wooys': {
                'handlers': ['file'],
                'level': 'INFO',
            },
        },

        # ハンドラ
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(BASE_DIR, 'logs/django.log'),
                'formatter': 'prod',
                'when': 'D',
                'interval': 1,
                'backupCount': 7,
            },
        },


        # フォーマッター
        'formatters': {
            'prod': {
                'format': '\t'.join([
                    '%(asctime)s',
                    '[%(levelname)s]',
                    '%(pathname)s(Line:%(lineno)d)',
                    '%(message)s'
                ])
            }
        },
    }


INTERNAL_IPS = ['127.0.0.1', '172.26.0.1']


def show_toolbar(request):
    return True


SHOW_TOOLBAR_CALLBACK = show_toolbar
