import time

class Timer:
    def __init__(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.stop_time = time.perf_counter()
        self.elapsed_time = self.stop_time - self.start_time
        return self.elapsed_time

    def reset(self):
        self.start_time = time.perf_counter()
        self.elapsed_time = None
        self.stop_time = None        
