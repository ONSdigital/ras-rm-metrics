import atexit
import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from metrics.rabbitmq import RabbitMQ


class Logger:
    def info(self, logger, message):
        logging.getLogger(logger).info(message)

    def error(self, logger, message):
        logging.getLogger(logger).error(message)


def init(frequency, debug):
    logging.debug("Starting scheduler...")
    scheduler = BackgroundScheduler()
    scheduler.start()

    rabbitmq = RabbitMQ(Logger(),
                        os.getenv('RABBITMQ_SERVICE_NAME', 'rabbitmq'))

    scheduler.add_job(
        func=lambda : rabbitmq.log_metrics(),
        trigger=IntervalTrigger(seconds=int(frequency)),
        id='rabbit_metrics',
        name='Print queue stats for all RabbitMQ queues.',
        replace_existing=True)

    if not debug:
        logging.getLogger('apscheduler').setLevel(logging.WARNING)

    atexit.register(lambda: scheduler.shutdown())
