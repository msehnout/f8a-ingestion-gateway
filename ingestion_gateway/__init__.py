"""Ingestion gateway module."""

# std imports:
import logging
import os
import sys

from f8a_mb import MbConsumer
from f8a_mb.path import topic_release_monitoring_pypi_get_listener


def set_up_logger():
    """Set up logging."""
    loglevel = os.environ.get('LOGLEVEL', 'INFO').upper()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger = logging.getLogger('release_monitor')
    logger.setLevel(loglevel)
    logger.addHandler(handler)
    return logger


logger = set_up_logger()


class Gateway:
    """Encapsulates a gateway to the ingestion pipeline."""

    def __init__(self):
        """Construct a new gateway instance."""
        self.consumer = MbConsumer([topic_release_monitoring_pypi_get_listener('Gateway')])

    def run(self):
        """Run it."""
        while True:
            try:
                msg = self.consumer.next_message()
                dict = msg.dict()
                logger.debug("Received: {}".format(dict))
            except KeyError:
                continue
            except KeyboardInterrupt:
                self.consumer.disconnect()
                exit(0)

