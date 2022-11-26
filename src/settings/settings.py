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
