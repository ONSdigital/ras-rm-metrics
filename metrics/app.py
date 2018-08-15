import json
import logging
import os
import sys

from flask import Flask
from flask import Response

from metrics import scheduler

log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

logging.basicConfig(stream=sys.stdout, level=log_level)

app = Flask(__name__)

scheduler_frequency = os.getenv('SCHEDULER_FREQUENCY', 'OFF')

if scheduler_frequency == 'OFF':
    logging.warning('Scheduler disabled')
else:
    scheduler.init(int(scheduler_frequency), log_level == 'DEBUG')


@app.route('/info')
def status():
    body = dict(name='ras-rm-metrics', status='OK')

    response = Response(json.dumps(body))
    response.headers['Content-Type'] = 'application/json'

    return response
