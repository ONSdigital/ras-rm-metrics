import atexit
import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from metrics.rabbitmq import RabbitMQ
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))


def init(frequency, debug):
    logger.debug("Starting scheduler...")
    scheduler = BackgroundScheduler()
    scheduler.start()

    rabbitmq = RabbitMQ(os.getenv('RABBITMQ_SERVICE_NAME', 'rabbitmq'))

    scheduler.add_job(
        func=lambda: rabbitmq.log_metrics(),
        trigger=IntervalTrigger(seconds=int(frequency)),
        id='rabbit_metrics',
        name='Print queue stats for all RabbitMQ queues.',
        replace_existing=True)

    if not debug:
        logging.getLogger('apscheduler').setLevel(logging.ERROR)

    atexit.register(lambda: scheduler.shutdown())
