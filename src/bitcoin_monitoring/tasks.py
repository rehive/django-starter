import requests
from celery import shared_task

import logging

from django.db import transaction
from two1.blockchain.exceptions import DataProviderError

from .api import BitcoinMonitoringInterface
from .exceptions import WebhookFailedError
from .models import Webhook, Transaction

from celery.signals import worker_process_init, worker_process_shutdown
logger = logging.getLogger('django')

@worker_process_init.connect
def init_worker(**kwargs):
    global bitcoin_interface
    logger.info('Initializing HTTP session for worker.')
    bitcoin_interface = BitcoinMonitoringInterface()


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    global bitcoin_interface
    if bitcoin_interface:
        logger.info('Closing HTTP session for worker.')
        bitcoin_interface.provider.session.close()

@shared_task
def process_new():
    for webhook in Webhook.objects.all():
        new_transaction_notifications.delay(webhook.id)

@shared_task()
def process_confirmations():
    txs = Transaction.objects.filter(status='Processing')
    for tx in txs:
        confirmation_notifications.delay(tx.id)

@shared_task
def new_transaction_notifications(webhook_id):
    global bitcoin_interface
    webhook = Webhook.objects.get(id=webhook_id)
    logger.info('Checking for new transactions for %s' % webhook.address)
    interface = bitcoin_interface

    # Get all transactions for address, starting from last block checked
    txs = interface.get_transactions([webhook.address], min_block=webhook.last_block)
    block_height = interface.get_block_height()

    # For each transaction initiate a webhook task
    for tx_data in txs[webhook.address]:
        tx, created = Transaction.objects.get_or_create(tx_code=tx_data['hash'],
                                                        webhook=webhook)
        if created:
            with transaction.atomic():
                logger.info('New transaction detected: %s' % tx_data['hash'])
                tx = Transaction.objects.select_for_update().get(id=tx.id)
                tx.data = tx_data
                tx.confirmations = tx_data['confirmations']
                tx.status = 'Detected'
                tx.notifications = 0
                tx.save()

            #  Separated as this might fail due to SQS issues
            try:
                with transaction.atomic():
                    tx = Transaction.objects.select_for_update().get(id=tx.id)
                    transaction_webhook.delay(tx.id, tx.webhook.url, tx.webhook.secret)
                    tx.status = 'Processing'
                    tx.notifications = 1
                    tx.save()
            except Exception as exc:
                logger.info('Unhandled exception')
                logger.exception(exc)

    with transaction.atomic():
        logger.info('Webhook block height updated')
        webhook = Webhook.objects.select_for_update().get(id=webhook.id)
        webhook.last_block = block_height
        webhook.save()


@shared_task
def confirmation_notifications(tx_id):
    global bitcoin_interface
    logger.info('Confirmation Notification')

    with transaction.atomic():
        tx = Transaction.objects.select_for_update().get(id=tx_id)
        if tx.confirmations > tx.webhook.confirmations:
            logger.info('Already more confirmations than notification threshold')
            logger.info('Transaction complete')
            tx.status = 'Complete'
            tx.save()
        elif tx.notifications <= tx.webhook.confirmations:
            interface = bitcoin_interface
            try:
                tx_data = interface.get_transactions_by_id([tx.tx_code])[tx.tx_code]
                if tx_data['confirmations'] > tx.confirmations:
                    tx.confirmations = tx_data['confirmations']
                    tx.data = tx_data
                    tx.notifications += 1
                    tx.save()
                    transaction_webhook.delay(tx.id, tx.webhook.url, tx.webhook.secret)
                elif tx_data['confirmations'] < tx.confirmations:
                    raise Exception("Error: confirmation inconsistency on tx %s" % tx.tx_code)
            except DataProviderError:
                # TODO: Update this to only catch 404
                tx.status = 'Error'
                tx.save()
        else:
            logger.info('Confirmation notification threshold reached')
            logger.info('Transaction complete')
            tx.status = 'Complete'
            tx.save()

    if tx.status == "Error":
        raise Exception('Possible double spend transaction detected %s' % tx.tx_code)


@shared_task(bind=True, name='address_monitoring.webhook', max_retries=24, default_retry_delay=60 * 60)
def transaction_webhook(self, tx_id, url, secret):
    logger.info('Sending transaction webhook notification.')
    # Authorization header:
    if secret:
        headers = {'Authorization': 'Secret ' + secret}
    else:
        headers = {}

    tx = Transaction.objects.get(id=tx_id)
    #  TODO: perhaps rather update tx.notifications here

    # Handle webhook request and attempts
    try:
        r = requests.post(url, json=tx.data, headers=headers, timeout=5)

        if r.status_code == 200:
            pass  # Transaction successfully received by webhook
        else:
            try:
                self.retry(exc=WebhookFailedError)
            except WebhookFailedError:
                logger.info('Final transaction webhook task failure due to non 200 response.')

    except requests.exceptions.RequestException as e:
        try:
            self.retry(countdown=5 * 60, exc=WebhookFailedError)
        except WebhookFailedError:
            logger.info('Final transaction webhook task failure due to connection error.')

    return True
