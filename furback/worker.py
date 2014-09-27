import signal
import threading
import logging
import time

from furback.db import DB
from furback.api import ApiServer
from furback.runner import Runner

class Worker(object):
    def start(self):
        self.logger = logging.getLogger(__name__)

        self.run_lock = threading.Lock()
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)

        messages = [None, None]

        self.db = DB()

        self.api = ApiServer(messages)
        self.api.start()

        self.scripts = self.db.get_scripts()
        whee = 0

        while self.run_lock.acquire(False):
            try:
                whee += 1
                if whee % 100 == 0:
                    changes = self.db.get_changes()
                    if changes is not None:
                        self.scripts = self.db.get_scripts()

                out = messages[0]
                if out:
                    print("received: %s" % out)
                    messages[0], messages[1] = None, self.process(out)

            finally:
                self.run_lock.release()

            time.sleep(0.01)

        print("goodbye")

    def process(self, text):
        if "weather" in text:
            return "say It's always sunny in Philadelphia"
        elif "improv" in text:
            return "say Yes and\nwait 100\ndo 868"

        return "say four oh four Not found"

    def cleanup(self, signal, frame):
        self.run_lock.acquire()
        self.api.stop()
