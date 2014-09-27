import threading
import sys

class SuperThreadStoppingException(Exception):
    """ This exception is used to interrupt a running SuperThread. """
    pass

class SuperThread(threading.Thread):
    """ An opinionated thread class.

    The goal of `SuperThread` is to simplify thread management by providing clear
    ways to start, stop and sleep a concurrent operation.

    Additionally `SuperThread` provides exception tracking which allows you to
    re-raise or inspect an exception that caused the thread to exit.

    Usage::

        class FooThread(SuperThread):
            def setup(self):
                self.foo = "bar"

            def sleep(self):
                time.sleep(1)

            def work(self):
                do_work()

            def cleanup(self):
                do_cleanup()

        foo = FooThread()
        foo.start()         # start a foo thread
        time.sleep(5)       # let it execute for 5 seconds
        foo.stop()          # signal foo to stop as soon as possible
        foo.join()          # block forever while foo stops
    """

    sleep = None

    def __init__(self):
        threading.Thread.__init__(self)
        self._starting = True
        self._stopping = threading.Event()
        self._exception = None

        if self.sleep is None:
            raise NotImplementedError("%s must specify the SuperThread.sleep property" % self)

    def run(self):
        """ `run()` manages the main `SuperThread` execution loop. """
        try:
            self.setup()
            self._starting = False
            try:
                while not self._stopping.wait(self.sleep):
                    self.work()
            except SuperThreadStoppingException:
                pass
            self.cleanup()
        except Exception:
            self._exception = sys.exc_info()
            raise

    def setup(self):
        """ `setup()` runs once in the thread before any calls to work happen. """
        pass

    def work(self):
        """ `work()` runs between calls to `sleep()`. """
        raise NotImplementedError("%s must override SuperThread.work()" % self)

    def cleanup(self):
        """ `cleanup()` runs once in the thread before the thread stops.

        Note: Cleanup does not run if the thread exits due to an exception!
        """
        pass

    def starting(self):
        """ Returns ``True`` if the thread is currently starting. """
        return self._starting

    def stopping(self):
        """ Returns ``True`` if the thread is currently stopping. """
        return self._stopping.is_set()

    def stop(self):
        """ Signals the thread to stop as early as possible. """
        self._stopping.set()

    def interrupt_if_stopping(self):
        """ Raises `SuperThreadStoppingException` if the thread is stopping.

        If `SuperThreadStoppingException` is raised in `work()` or `sleep()` it
        will interrupt execution and cause the thread to stop.

        Usage::

            class Foo(SuperThread):
                def work(self):
                    for i in range(100):
                        super_slow_process(i)
                        # this call to interrupt_if_stopping will allow us to interrupt
                        # the slow process if we should actually be stopping.
                        self.interrupt_if_stopping()
        """
        if self.stopping():
            raise SuperThreadStoppingException()

    def has_exception(self):
        """ Return ``True`` if the thread exited due to an exception. """
        return self._exception is not None

    def get_exception(self):
        """ If the thread exited due to an exception, return the exception instance. """
        _, exc_inst, traceback = self._exception
        return exc_inst.with_traceback(traceback)

    def get_exc_info(self):
        """ If the thread exited due to an exception, return the exc_info. """
        return self._exception

    def check_exception(self):
        """ Re-raises the exception that caused the thread to exit if there was one. """
        if self._exception is not None:
            raise self.get_exception()
