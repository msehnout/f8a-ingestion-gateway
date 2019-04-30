import logging
from datetime import datetime

logger = logging.getLogger('release_monitor')


class DebugOutput:

    def __init__(self):
        self.packages = set()
        self.last_dump = datetime.now()

    def dump(self):
        for i in sorted(self.packages):
            logger.info("### Packages dump: {}".format(i))

        self.packages = set()

    def insert(self, pkg: str):
        self.packages.add(pkg)
        now = datetime.now()
        if now.minute != self.last_dump.minute:
            self.dump()
            self.last_dump = now
