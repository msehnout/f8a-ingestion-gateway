"""Ingestion gateway module."""

# std imports:
import logging
import os
import sys


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

    def run(self):
        """Run it."""
