import os

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')

ANYMAIL = {
    "SENDGRID_API_KEY": SENDGRID_API_KEY,
}

EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"

SERVER_EMAIL = 'Example <info@example.com>'
DEFAULT_FROM_EMAIL = 'Example <info@example.com>'

if os.environ.get('ENV_FILE', '') == '.local.env':
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
