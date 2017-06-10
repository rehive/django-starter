import os

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')

ANYMAIL = {
    "SENDGRID_API_KEY": SENDGRID_API_KEY,
}

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
CELERY_EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"

SERVER_EMAIL = 'Rehive Server <info@rehive.com>'
DEFAULT_FROM_EMAIL = 'Rehive <info@rehive.com>'

project_id = os.environ.get('CELERY_ID', 'local')
notification_queue = '-'.join(('notification', project_id))

CELERY_EMAIL_TASK_CONFIG = {
    'queue': notification_queue,
    'name': 'async_email_send',
    'ignore_result': True,
}

ADMINS = [('Michail', 'michail@rehive.com'),
          ('Helghardt', 'helghardt@rehive.com'),
          ('Joshua', 'joshua@rehive.com')]
