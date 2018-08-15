import json

import cfenv
import requests


class RabbitMQ:
    def __init__(self, logger, cf_service_name):
        self.logger = logger
        self.cf_service_name = cf_service_name

    def log_metrics(self):
        for service_name, uri in self._get_services_from_cf().items():
            queues = self._fetch_metrics_for_all_queues(service_name, uri)

            for queue_metrics in queues:
                self._log_queue_metrics(service_name, queue_metrics)

    def _get_services_from_cf(self):
        return {s.name: s.credentials['http_api_uri']
                for s in cfenv.AppEnv().services
                if cfenv.match_all(s.env, {'label': self.cf_service_name})}

    def _fetch_metrics_for_all_queues(self, service, uri):
        uri = uri.rstrip('/') + '/queues'
        response = requests.get(uri)

        if response.status_code != requests.codes.ok:
            self.logger.error(
                self._service_logger_name(service),
                f'GET {uri} - [{response.status_code}] - {response.text}')
            return []

        return [self._prepare_metrics(service, metrics) for metrics in
                response.json()]

    def _prepare_metrics(self, service, raw):
        return {
            'service': service,
            'name': raw['name'],
            'messages': raw['messages']
        }

    def _log_queue_metrics(self, service_name, queue_metrics):
        self.logger.info(
            self._queue_logger_name(service_name, queue_metrics['name']),
            json.dumps({'messages': queue_metrics['messages']}))

    def _queue_logger_name(self, service_name, queue_name):
        return f'{self._service_logger_name(service_name)}.{queue_name}'

    def _service_logger_name(self, service):
        return f'sdc.metrics.{self.cf_service_name}.{service}'
