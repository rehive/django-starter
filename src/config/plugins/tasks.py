from datetime import timedelta
import os
from logging import getLogger

logger = getLogger('django')

if os.environ.get('SKIP_TASK_QUEUE') in ['True', 'true', True]:
    logger.info('Task Queues Disabled')
    CELERY_ALWAYS_EAGER = True
else:
    logger.info('Task Queues Enabled')

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "UTC"

CELERY_CREATE_MISSING_QUEUES = True
CELERYD_PREFETCH_MULTIPLIER = 150
BROKER_CONNECTION_TIMEOUT = 10.0

CELERY_TASK_SERIALIZER = 'msgpack'
CELERY_ACCEPT_CONTENT = ['msgpack', 'json']

celery_id = os.environ.get('CELERY_ID', 'local')
default_queue = '-'.join(('general', celery_id))

CELERY_DEFAULT_QUEUE = default_queue

queue_1 = '-'.join(('queue-1', celery_id))

CELERY_ROUTES = {'starter.tasks.test': {'queue': queue_1},}

BROKER_TRANSPORT = 'sqs'
BROKER_TRANSPORT_OPTIONS = {
    'region': 'eu-west-1',
    'visibility_timeout': 43200,
    'polling_interval': 0.01,
}

CELERYBEAT_SCHEDULE = {
    'scheduled_task': {
        'task': 'starter.tasks.test',
        'schedule': timedelta(seconds=5),
        'args': ()
    },
}
