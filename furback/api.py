from tornado import gen
from tornado import web
from tornado import httpserver
from tornado import ioloop

from furback.super_thread import SuperThread

class ApiHttpHandler(web.RequestHandler):
    def initialize(self, worker):
        self.worker = worker

    @gen.coroutine
    def get(self):
        text = self.get_argument("text")
        out = yield self.worker.process(text.lower())
        print("sending: %s" % out)
        self.finish(out)

class ApiServer(SuperThread):
    sleep = 0

    def __init__(self, worker):
        self.worker = worker
        SuperThread.__init__(self)

    def setup(self):
        self._loop = ioloop.IOLoop()
        self._host = "0.0.0.0"
        self._port = 9000
        self._routes = [
            (r"/", ApiHttpHandler, { "worker": self.worker })
        ]

    def work(self):
        app = web.Application(handlers=self._routes)

        server = httpserver.HTTPServer(request_callback=app, io_loop=self._loop)
        server.listen(address=self._host, port=self._port)

        print("Listening on %s:%d" % (self._host, self._port))

        self._set_interval(self._check_closed, 1000)

        self._loop.start()

    def _set_interval(self, callback, interval):
        cb = ioloop.PeriodicCallback(callback, interval, io_loop=self._loop)
        cb.start()

    def _check_closed(self):
        if self.stopping():
            self._loop.stop()
