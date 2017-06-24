import requests
from celery import shared_task

import logging

logger = logging.getLogger('django')


@shared_task()
def test():
    print('Hello World')
    return True