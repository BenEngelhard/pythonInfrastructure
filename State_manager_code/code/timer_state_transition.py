import threading
import time

class StateTimer:
    def __init__(self, timeout_duration):
        self.timeout_duration = timeout_duration
        self.start_time = None
        self.timer_thread = None
        self.done = threading.Event()

    def start(self):
        self.start_time = time.time()
        self.done.clear()
        self.timer_thread = threading.Timer(self.timeout_duration, self._times_up)
        self.timer_thread.start()

    def _times_up(self):
        self.done.set()

    def stop(self):
        if self.timer_thread is not None:
            self.timer_thread.cancel()
        self.done.clear()

    def reset(self):
        self.stop()
        self.start()

    def is_done(self):
        return self.done.is_set()

    def time_elapsed(self):
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

    def remaining_time(self):
        elapsed = self.time_elapsed()
        return max(0, self.timeout_duration - elapsed)
za