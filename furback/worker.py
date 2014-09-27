import signal
import threading
import time
import os
import logging

from furback.db import DB

from client import vocabcompiler, tts, stt, jasperpath
from client.conversation import Conversation
from client.mic import Mic

class Worker(object):
    def __init__(self):
        self.db = DB()

    def start(self):
        self.logger = logging.getLogger(__name__)

        self.run_lock = threading.Lock()
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)

        api_key = "conor to fill in"
        stt_engine_type = "google"
        tts_engine_slug = tts.get_default_engine_slug()
        tts_engine_class = tts.get_engine_by_slug(tts_engine_slug)

        # Compile dictionary
        sentences, dictionary, languagemodel = [os.path.abspath(os.path.join(jasperpath.LIB_PATH, filename)) for filename in ("sentences.txt", "dictionary.dic", "languagemodel.lm")]
        vocabcompiler.compile(sentences, dictionary, languagemodel)

        mic = Mic(tts_engine_class, stt.PocketSphinxSTT(), stt.newSTTEngine(stt_engine_type, api_key=api_key))

        mic.say("Hello!")

        while self.run_lock.acquire(False):
            try:
                print("hello world")
            finally:
                self.run_lock.release()

            time.sleep(1)

        print("goodbye")

    def cleanup(self, signal, frame):
        self.run_lock.acquire()
