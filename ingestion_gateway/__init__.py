"""Ingestion gateway module."""

# std imports:
import logging
import os
import sys

import requests

from f8a_mb import MbConsumer
from f8a_mb.path import topic_release_monitoring_pypi_get_listener,\
                        topic_release_monitoring_npm_get_listener

from ingestion_gateway.debug_output import DebugOutput


API_SERVER = os.environ.get('API_SERVER', 'http://localhost:8080')


def set_up_logger():
    """Set up logging."""
    loglevel = os.environ.get('LOGLEVEL', 'INFO').upper()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger = logging.getLogger('ingestion_gateway')
    logger.setLevel(loglevel)
    logger.addHandler(handler)
    return logger


logger = set_up_logger()


class Gateway:
    """Encapsulates a gateway to the ingestion pipeline."""

    def __init__(self):
        """Construct a new gateway instance."""
        self.consumer = MbConsumer([topic_release_monitoring_pypi_get_listener('Gateway'),
                                    topic_release_monitoring_npm_get_listener('Gateway')])
        self.debug_output = DebugOutput()

    def run(self):
        """Run it."""
        logger.info("Starting")
        while True:
            try:
                msg = self.consumer.next_message()
                dict = msg.dict()
                logger.info("Sending this to the ingestion API: {}".format(dict))
                r = requests.post('{}/submit'.format(API_SERVER), json=dict)
                if r.status_code != 200:
                    logger.warning('Failed to submit the data (code {})'.format(r.status_code))

                self.debug_output.insert(msg.content)
            except KeyError:
                continue
            except KeyboardInterrupt:
                self.consumer.disconnect()
                exit(0)
