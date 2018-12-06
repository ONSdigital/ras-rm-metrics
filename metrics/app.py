import json
import logging
import os

from flask import Flask
from flask import Response
from structlog import wrap_logger

from metrics import scheduler
from metrics.logger_config import logger_initial_config

log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logger = wrap_logger(logging.getLogger(__name__))
logger_initial_config(service_name='ras-rm-metrics', log_level=log_level)

app = Flask(__name__)

scheduler_frequency = os.getenv('SCHEDULER_FREQUENCY', 'OFF')

if scheduler_frequency == 'OFF':
    logger.warning('Scheduler disabled')
else:
    logger.info('Starting metrics service...', scheduler_frequency=scheduler_frequency)
    scheduler.init(int(scheduler_frequency), log_level == 'DEBUG')


@app.route('/info')
def status():
    body = dict(name='ras-rm-metrics', status='OK')

    response = Response(json.dumps(body))
    response.headers['Content-Type'] = 'application/json'

    return response
