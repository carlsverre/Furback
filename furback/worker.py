import signal
import threading
import logging
import time
import os
import json
import glob
import re

from furback.db import DB
from furback.api import ApiServer
from furback.runner import Runner
from furback import tiara

bad_stuff = re.compile(r"[\.,-\/#!$%\^&\*;\?:{}=\-_`~()]")

class Worker(object):
    def start(self):
        self.logger = logging.getLogger(__name__)
        self.runner_index = {}

        self.run_lock = threading.Lock()
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)

        messages = [None, None]

        self.db = DB()

        self.api = ApiServer(messages)
        self.api.start()

        for script in glob.glob("./modules/*.py"):
            meta = json.loads(open(script + ".meta").read())
            self.db.save_script(os.path.basename(script).rstrip(".py"), open(script).read(), meta['priority'], meta['words'])

        self.load_scripts()
        whee = 0

        while self.run_lock.acquire(False):
            try:
                whee += 1
                if whee % 100 == 0:
                    changes = self.db.get_changes()
                    if changes is not None:
                        self.load_scripts()

                out = messages[0]
                if out:
                    print("received: %s" % out)
                    messages[0], messages[1] = None, self.process(out)

            finally:
                self.run_lock.release()

            time.sleep(0.01)

        print("goodbye")

    def load_scripts(self):
        scripts = self.db.get_scripts()
        index = {}

        for script in scripts:
            for word in script['words']:
                if word:
                    word = word.lower()
                    if word in index:
                        if index[word]['priority'] < script['priority']:
                            index[word] = script
                    else:
                        index[word] = script

        self.index = index

    def process(self, text):
        runner = None
        script = None
        for word in re.sub(bad_stuff, "", text).split(" "):
            word = word.strip().lower()
            if word:
                for key in self.runner_index.keys():
                    if key in word:
                        if self.runner_index[key].running():
                            print "picking runner %s because %s" % (key, word)
                            runner = self.runner_index[key]
                            break
                        else:
                            del self.runner_index[key]

                for key in self.index.keys():
                    if key in word:
                        print "picking script %s because %s" % (key, word)
                        script = self.index[key]
                        break

        if script is None and runner is None:
            return "not found; %s" % tiara.Respond(text)

        if runner is None:
            print("creating new runner")
            runner = Runner(script['body'])
            runner.run()
            runner.write(text)
        else:
            print("found existing runner")
            runner.write(text)

        out = ""
        while runner.running():
            next_read = runner.read().strip()
            if "listen_for" in next_read:
                _, words = next_read.split(" ")
                words = words.split(",")
                for word in words:
                    if word:
                        print("adding %s" % word)
                        self.runner_index[word.lower()] = runner
                break
            elif next_read:
                print("got: %s" % next_read)
                out += next_read + "\n"

        return out.strip() + "\n"

    def cleanup(self, signal, frame):
        self.run_lock.acquire()
        self.api.stop()
