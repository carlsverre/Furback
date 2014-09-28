import signal
import threading
import logging
import time
import os
import json
import glob

from wraptor.decorators import throttle

from tornado.concurrent import Future

from furback.db import DB
from furback.api import ApiServer
from furback.runner import Runner
from furback.index import Index
from furback import tiara

from collections import deque

class Worker(object):
    def start(self):
        self._running = True
        self.logger = logging.getLogger(__name__)
        self.index = Index()

        self.process_queue = deque()

        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)

        self.db = DB()

        self.api = ApiServer(self)
        self.api.start()

        # load scripts from filesystem into db
        for script in glob.glob("./modules/*.py"):
            meta = json.loads(open(script + ".meta").read())
            self.db.save_script(os.path.basename(script).rstrip(".py"), open(script).read(), meta['priority'], meta['words'])

        while self._running:
            self.load_scripts()

            try:
                text, future = self.process_queue.popleft()
                out = self._process(text)
                future.set_result(out)
            except IndexError:
                time.sleep(0.001)

        print("goodbye")

    @throttle(1, instance_method=True)
    def load_scripts(self):
        changes = self.db.get_changes()
        if changes is not None:
            scripts = self.db.get_scripts()
            for script in scripts:
                if len(script['words']):
                    self.index.script(script['name'], script['words'], script['priority'], script['body'])

    def process(self, text):
        future = Future()
        self.process_queue.append((text, future))
        return future

    def _process(self, text):
        print("Processing: `%s`" % text)
        match = self.index.lookup(text)

        if match is None:
            return "not found; %s" % tiara.Respond(text)

        if isinstance(match, str):
            # we have a script body!
            print("Creating new runner")
            runner = Runner(match)
            runner.run()
        else:
            runner = match

        print("Writing input `%s`" % text)
        runner.write(text)

        out = ""
        while runner.running():
            next_read = runner.read().strip()
            if next_read:
                if next_read.startswith("listen_for"):
                    _, words = next_read.split(" ", 1)
                    self.index.listen_for([w.strip().lower() for w in words.split(",")], runner)
                    break
                else:
                    print("Got: `%s`" % next_read)
                    out += next_read + "\n"

        return out.strip() + "\n"

    def cleanup(self, signal, frame):
        print("Exiting...")
        self._running = False
        self.api.stop()
