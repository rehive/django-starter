import os

if os.environ.get('POSTGRES_PORT'):
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
elif os.environ.get('DATABASE_PGPOOL_SERVICE_PORT_5432_TCP_PORT'):
    POSTGRES_PORT = os.environ.get('DATABASE_PGPOOL_SERVICE_PORT_5432_TCP_PORT')
elif os.environ.get('DATABASE_POSTGRES_SERVICE_PORT_5432_TCP_PORT'):
    POSTGRES_PORT = os.environ.get('DATABASE_POSTGRES_SERVICE_PORT_5432_TCP_PORT')
elif os.environ.get('POSTGRES_1_PORT_5432_TCP_PORT'):
    POSTGRES_PORT = os.environ.get('POSTGRES_1_PORT_5432_TCP_PORT')
else:
    POSTGRES_PORT = 5432

if os.environ.get('POSTGRES_HOST'):
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
elif os.environ.get('DATABASE_PGPOOL_SERVICE_SERVICE_HOST'):
    POSTGRES_HOST = os.environ.get('DATABASE_PGPOOL_SERVICE_SERVICE_HOST')
elif os.environ.get('DATABASE_POSTGRES_SERVICE_SERVICE_HOST'):
    POSTGRES_HOST = os.environ.get('DATABASE_POSTGRES_SERVICE_SERVICE_HOST')
elif os.environ.get('POSTGRES_PORT_5432_TCP_ADDR'):
    POSTGRES_HOST = os.environ.get('POSTGRES_PORT_5432_TCP_ADDR')
else:
    POSTGRES_HOST = 'localhost'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
