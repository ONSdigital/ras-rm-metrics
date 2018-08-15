import json
import os
import unittest
from unittest.mock import Mock, call

import httpretty

from rabbitmq import RabbitMQ


class Test(unittest.TestCase):
    def tearDown(self):
        os.unsetenv('VCAP_SERVICES')

    @httpretty.activate
    def test_log_metrics(self):
        os.environ['VCAP_SERVICES'] = json.dumps({
            "rabbitmq": [
                {
                    "credentials": {
                        "http_api_uri": "http://example.com/rabbit1/api/",
                    },
                    "label": "rabbitmq",
                    "name": "rm-rabbitmq",
                },
                {
                    "credentials": {
                        "http_api_uri": "http://example.com/rabbit2/api/",
                    },
                    "label": "rabbitmq",
                    "name": "sdx-rabbitmq",
                }
            ]
        })

        metrics1 = [
            {"messages": 101, "reductions": 7654321, "name": "queue1"},
            {"messages": 202, "reductions": 1234567, "name": "queue2"}
        ]

        metrics2 = [
            {"messages": 303, "reductions": 6666666, "name": "queue3"}
        ]

        httpretty.register_uri(
            httpretty.GET,
            'http://example.com/rabbit1/api/queues',
            body=json.dumps(metrics1),
            status=200
        )

        httpretty.register_uri(
            httpretty.GET,
            'http://example.com/rabbit2/api/queues',
            body=json.dumps(metrics2),
            status=200
        )

        logger = Mock()

        RabbitMQ(logger, 'rabbitmq').log_metrics()

        logger.info.assert_has_calls(
            [
                call('sdc.metrics.rabbitmq.rm-rabbitmq.queue1',
                     '{"messages": 101}'),
                call('sdc.metrics.rabbitmq.rm-rabbitmq.queue2',
                     '{"messages": 202}'),
                call('sdc.metrics.rabbitmq.sdx-rabbitmq.queue3',
                     '{"messages": 303}')
            ]
        )

    @httpretty.activate
    def test_log_metrics_works_without_trailing_slashes_on_the_uris(self):
        os.environ['VCAP_SERVICES'] = json.dumps({
            "rmq-service": [
                {
                    "credentials": {
                        "http_api_uri": "http://example.com/api",
                    },
                    "label": "rmq-service",
                    "name": "rm-rabbitmq",
                }
            ]
        })

        metrics = [
            {'messages': 101, 'reductions': 7654321, 'name': 'queue1'},
        ]

        httpretty.register_uri(
            httpretty.GET,
            'http://example.com/api/queues',
            body=json.dumps(metrics),
            status=200
        )

        logger = Mock()

        RabbitMQ(logger, 'rmq-service').log_metrics()

        logger.info.assert_has_calls(
            [
                call('sdc.metrics.rmq-service.rm-rabbitmq.queue1',
                     '{"messages": 101}')
            ]
        )

    @httpretty.activate
    def test_log_metrics_raises_for_http_errors(self):
        os.environ['VCAP_SERVICES'] = json.dumps({
            "rabbitmq": [
                {
                    "credentials": {
                        "http_api_uri": "http://example.com/api",
                    },
                    "label": "rabbitmq",
                    "name": "rm-rabbitmq",
                }
            ]
        })

        httpretty.register_uri(
            httpretty.GET,
            'http://example.com/api/queues',
            body='Error text',
            status=500
        )

        logger = Mock()

        RabbitMQ(logger, 'rabbitmq').log_metrics()

        logger.error.assert_has_calls(
            [
                call('sdc.metrics.rabbitmq.rm-rabbitmq',
                     f'GET http://example.com/api/queues - [500] - Error text')
            ]
        )
