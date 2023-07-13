import threading
import time
class CustomThread(threading.Thread):
    def __init__(self, target=None, delay=1,*args):
        super().__init__()
        self.target = target
        self.args = args
        self.delay = delay
        self.delaySleep=delay
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            self.delaySleep=self.delay
            if self.target is not None:
                self.target(*self.args)
            while self.delaySleep>0:
                self.delaySleep-=1
                time.sleep(1)


    def stop(self):
        self._stop_event.set()
        self.delaySleep=0


