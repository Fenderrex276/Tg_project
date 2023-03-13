import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'postgres',
        'PORT': 5432,
    }
}

INSTALLED_APPS = (
    'db',
)

SECRET_KEY = 'ogew78f887fho273f1o3f(&*^&%Y(&*^G&fr46'

TOKEN_CLIENT = os.getenv('TOKEN_CLIENT')
TOKEN_ADMIN = os.getenv('TOKEN_ADMIN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
DEBUG = True if  os.getenv('DEBUG') == 'True' else False
TEST = True if  os.getenv('TEST') == 'True' else False
PATH_TO_CLIENT_LOG = os.environ.get('PATH_TO_CLIENT_LOG')
PATH_TO_ADMIN_LOG = os.environ.get('PATH_TO_ADMIN_LOG')
PATH_TO_LOG = os.environ.get('PATH_TO_LOG')
PATH_TO_APSCHEDULER_LOG = os.environ.get('PATH_TO_APSCHEDULER_LOG')
PATH_TO_AIOGRAM_LOG = os.environ.get('PATH_TO_AIOGRAM_LOG')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'high': {
            'format': '{asctime} {levelname} {name} [line {lineno}] {message}',
            'style': '{',
        },
        'low': {
            'format': '{asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'log_file': {
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'high',
            'filename': PATH_TO_LOG,
            'maxBytes': 1024 * 1024 * 500,  # 500 Mb
            'backupCount': 10
        },
        'client_file': {
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'high',
            'filename': PATH_TO_CLIENT_LOG,
            'maxBytes': 1024 * 1024 * 500,  # 500 Mb
            'backupCount': 10
        },
        'apscheduler_file': {
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'high',
            'filename': PATH_TO_APSCHEDULER_LOG,
            'maxBytes': 1024 * 1024 * 500,  # 500 Mb
            'backupCount': 10
        },
        'aiogram_file': {
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'high',
            'filename': PATH_TO_AIOGRAM_LOG,
            'maxBytes': 1024 * 1024 * 500,  # 500 Mb
            'backupCount': 10
        },
        'admin_file': {
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'high',
            'filename': PATH_TO_ADMIN_LOG,
            'maxBytes': 1024 * 1024 * 500,  # 500 Mb
            'backupCount': 10
        },

        'console': {
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'high'
        },
    },
    'loggers': {
        'root': {
            'handlers': ['log_file'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
        },
        'bot': {
            'handlers': ['console', 'client_file'] if DEBUG else ['client_file'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'propagate': False
        },
        'client': {
            'handlers': ['console', 'client_file'] if DEBUG else ['client_file'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'propagate': False
        },
        'apscheduler': {
            'handlers': ['console', 'apscheduler_file'] if DEBUG else ['apscheduler_file'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'propagate': False
        },
        'aiogram': {
            'handlers': ['console', 'aiogram_file'] if DEBUG else ['aiogram_file'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'propagate': False
        },
        'admin': {
            'handlers': ['console', 'admin_file'] if DEBUG else ['admin_file'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'propagate': False
        },


    }
}
