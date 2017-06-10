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

project_id = os.environ.get('CELERY_ID', 'local')
default_queue = '-'.join(('general', project_id))

CELERY_DEFAULT_QUEUE = default_queue

scheduled_processing_queue = '-'.join(('scheduled-processing', project_id))
notify_new_txs_queue = '-'.join(('notify-new-txs', project_id))
notify_confirmations_queue = '-'.join(('notify-confirmations', project_id))
send_webhooks_queue = '-'.join(('send-webhooks', project_id))

CELERY_ROUTES = {'bitcoin_monitoring.tasks.process_new': {'queue': scheduled_processing_queue},
                 'bitcoin_monitoring.tasks.process_confirmations': {'queue': scheduled_processing_queue},
                 'bitcoin_monitoring.tasks.new_transaction_notifications': {'queue': notify_new_txs_queue},
                 'bitcoin_monitoring.tasks.confirmation_notifications': {'queue': notify_confirmations_queue},
                 'bitcoin_monitoring.tasks.transaction_webhook': {'queue': send_webhooks_queue},}

BROKER_TRANSPORT = 'sqs'
BROKER_TRANSPORT_OPTIONS = {
    'region': 'eu-west-1',
    'visibility_timeout': 43200,
    'polling_interval': 0.01,
}

CELERYBEAT_SCHEDULE = {
    'bitcoin_process_new': {
        'task': 'bitcoin_monitoring.tasks.process_new',
        'schedule': timedelta(seconds=3),
        'args': ()
    },
    'bitcoin_process_confirmations': {
        'task': 'bitcoin_monitoring.tasks.process_confirmations',
        'schedule': timedelta(seconds=10)
    }
}
