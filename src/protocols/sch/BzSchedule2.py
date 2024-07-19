
import threading
from conf.logconfig import logger

class BzSchedule2(threading.Thread):
    def __init__(self):
        super().__init__()
        self.jobs = []
        self.lock = threading.Lock()
        self.stop_event = threading.Event()

    def add_task(self, task, *args, interval=1, unit='seconds'):
        with self.lock:
            job = schedule.every(interval)
            if unit == 'seconds':
                job = job.seconds
            elif unit == 'minutes':
                job = job.minutes
            elif unit == 'hours':
                job = job.hours
            else:
                raise ValueError("Unsupported time unit.")
            job.do(self._create_worker, task, *args)
            self.jobs.append(job)

    def _create_worker(self, task, *args):
        worker = WorkerThread(len(self.jobs), task, *args)
        worker.start()

    def run(self):
        print("Scheduler started.")
        while not self.stop_event.is_set():
            with self.lock:
                schedule.run_pending()
            time.sleep(1)
        print("Scheduler stopped.")

    def stop(self):
        self.stop_event.set()