import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DATABASE_PGPOOL_SERVICE_SERVICE_HOST', 'postgres'),
        'PORT': os.environ.get('DATABASE_PGPOOL_SERVICE_PORT_5432_TCP_PORT', '5123'),
        'OPTIONS': {
            'connect_timeout': 3,
        }
    }
}
