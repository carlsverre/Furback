import logging
import time

from tornado import web
from tornado import httpserver
from tornado import ioloop

from furback.super_thread import SuperThread

logger = logging.getLogger(__name__)

class ApiHttpHandler(web.RequestHandler):
    def initialize(self, messages):
        self.messages = messages

    def get(self):
        text = self.get_argument("text")
        self.messages[0] = text
        self.messages[1] = None

        while self.messages[1] is None:
            time.sleep(0.001)

        out = self.messages[1]
        print("sending: %s" % out)
        self.finish(out)

class ApiServer(SuperThread):
    sleep = 0

    def __init__(self, messages):
        self.messages = messages
        SuperThread.__init__(self)

    def setup(self):
        self._loop = ioloop.IOLoop()
        self._host = "0.0.0.0"
        self._port = 9000
        self._routes = [
            (r"/", ApiHttpHandler, { "messages": self.messages })
        ]

    def work(self):
        app = web.Application(handlers=self._routes)

        server = httpserver.HTTPServer(request_callback=app, io_loop=self._loop)
        server.listen(address=self._host, port=self._port)

        logger.info("Listening on %s:%d", self._host, self._port)

        self._set_interval(self._check_closed, 1000)

        self._loop.start()

    def _set_interval(self, callback, interval):
        cb = ioloop.PeriodicCallback(callback, interval, io_loop=self._loop)
        cb.start()

    def _check_closed(self):
        if self.stopping():
            self._loop.stop()
